import json
from openai import OpenAI
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.conf import settings
from api.json.decision import handle_admin_command, execute_tool_call
from api.json.prompt import GENERAL_CONVERSATION_PROMPT, GENERAL_TELESELF_PROMPT, command_extraction_prompt
import cloudinary.uploader
from api.utils.openai_tools import ADMIN_TOOLS
import re
from api.models.product import Product

client = OpenAI(api_key=settings.OPENAI_API_KEY)

@csrf_exempt
def chatbot(request):
    if request.method != "POST":
        return JsonResponse({"error": "Only POST allowed"}, status=405)

    question = ""
    role = ""
    
    if request.content_type and 'multipart/form-data' in request.content_type:
        print(f"[CHATBOT] Xử lý request dạng multipart/form-data")
        question = request.POST.get('question', '')
        role = request.POST.get('role', '')
        is_form_submit = request.POST.get('is_form_submit', 'false') == 'true'
        print(f"[CHATBOT] Question: {question}")
        print(f"[CHATBOT] Role: {role}")
        
        uploaded_files = request.FILES.getlist('images')

        if uploaded_files:
            print(f"Đã nhận được {len(uploaded_files)} file ảnh. Bắt đầu upload lên Cloudinary...")
        
            for file in uploaded_files:
                try:
                    # Upload file lên Cloudinary
                    upload_result = cloudinary.uploader.upload(file)
                    # Lấy URL an toàn (secure_url) từ kết quả
                    image_url = upload_result['secure_url']
                    # In URL ra console để kiểm tra
                    print(f"  - Upload thành công file '{file.name}'. URL: {image_url}")
                    # Thêm URL vào danh sách để sử dụng sau
                    question += " " + image_url + " "
                except Exception as e:
                    # In ra lỗi nếu có
                    print(f"  - Lỗi khi upload file '{file.name}': {e}")
    else:
        # Nếu không có file, đọc như JSON thông thường
        try:
            data = json.loads(request.body)
            question = data.get("question", "")
            role = data.get("role", "")
            is_form_submit = data.get("is_form_submit", False)
        except json.JSONDecodeError:
            return JsonResponse({"error": "Invalid JSON payload"}, status=400)
    if role == 'user':
        # Prompt AI để trích xuất từ khóa tìm kiếm
        keyword_prompt = f"""
        Trích xuất từ khóa chính từ câu hỏi của người dùng để tìm kiếm sản phẩm trong database.
        Chỉ trả về từ khóa (ví dụ: 'iphone', 'samsung', 'tai nghe'), không giải thích hay thêm dấu câu.
        Câu hỏi: {question}
        """
        keyword_response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[{"role": "user", "content": keyword_prompt}],
            temperature=0,
            max_tokens=30
        )
        keyword = keyword_response.choices[0].message.content.strip()

        # Tìm kiếm bằng MongoEngine với phân biệt chữ hoa/thường (icontains)
        from mongoengine import Q
        
        # Tìm các sản phẩm có contains trong tên hoặc danh mục
        results = Product.objects(
            Q(name__icontains=keyword) | 
            Q(category__icontains=keyword) |
            Q(brand__icontains=keyword)
        ).limit(5)

        context = ""
        if results:
            for r in results:
                context += f"{r.name} - Danh mục: {r.category} (Giá: {r.price})\n"
        else:
            context = "Không tìm thấy sản phẩm nào khớp với yêu cầu trong cửa hàng.\n"

        # Gửi sang GPT
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content":  GENERAL_TELESELF_PROMPT},
                {"role": "user", "content": f"Câu hỏi: {question}\nDữ liệu sản phẩm:\n{context}"}
            ],
            max_tokens=200,
        )
        answer = response.choices[0].message.content
        return JsonResponse({"answer": answer})
    else:
        # True Agent: OpenAI Function Calling
        
        system_prompt = (
            "Bạn là AI Agent Admin thông minh quản lý cửa hàng TechHub. "
            "Nhiệm vụ của bạn là gọi các Func/Tools phù hợp theo yêu cầu của người dùng, hoặc trả lời tự nhiên nếu không có tool thích hợp. "
            "Khi sử dụng tool, luôn trả về tham số đúng định dạng JSON yêu cầu. "
            "ĐẶC BIỆT: Phân biệt rõ 'Tính năng nổi bật' (features: mảng các chuỗi, VD: ['Màn hình OLED', 'Pin 5000mAh']) "
            "và 'Thông số kỹ thuật' (specifications: object key-value, VD: {'Chip': 'A18', 'RAM': '8GB'}). "
            "Khi thấy người dùng yêu cầu 'mở trang', 'chuyển đến', 'đi tới', hãy sử dụng tool navigate_page. "
            "QUAN TRỌNG: Khi người dùng muốn thêm/tạo sản phẩm mới (dù chưa cung cấp đủ thông tin), "
            "hãy GỌI NGAY tool add_product với những thông tin có sẵn (ít nhất truyền name nếu biết). "
            "KHÔNG hỏi lại hay liệt kê yêu cầu — hệ thống sẽ tự hiện form để admin điền còn thiếu."
        )
        
        try:
            # Parse lịch sử chat từ frontend (nếu có)
            chat_history_raw = request.POST.get('chat_history', '[]')
            try:
                chat_history = json.loads(chat_history_raw)
                if not isinstance(chat_history, list):
                    chat_history = []
            except Exception:
                chat_history = []

            # Gửi tin nhắn sang GPT kèm theo lịch sử và tools
            messages = [
                {"role": "system", "content": system_prompt},
                *chat_history,  # Chèn lịch sử hội thoại trước câu hỏi hiện tại
                {"role": "user", "content": f"Câu hỏi/Yêu cầu: {question}"}
            ]
            response = client.chat.completions.create(
                model="gpt-4o-mini",
                messages=messages,
                tools=ADMIN_TOOLS,
                tool_choice="auto",
                max_tokens=600,
                temperature=0.2,
            )
            
            message = response.choices[0].message
            
            if message.tool_calls:
                # Trích xuất và chạy Tool
                tool_call = message.tool_calls[0]
                function_name = tool_call.function.name
                
                try:
                    function_args = json.loads(tool_call.function.arguments)
                except Exception as e:
                    function_args = {}
                    print(f"[TOOL PARSE ERROR] Lỗi phân tích JSON Argument: {e}")

                print(f"[AGENT ACTIVATED] AI Gọi hàm: {function_name} | Tham số: {function_args}")
                
                # Nếu AI muốn thêm sản phẩm nhưng chưa có ảnh (chưa upload),
                # trả về tín hiệu để frontend hiện inline form thay vì chạy ngay (trừ khi form đã được submit)
                if function_name == "add_product" and not function_args.get("images") and not is_form_submit:
                    prefill = {k: v for k, v in function_args.items() if k != "images"}
                    return JsonResponse({
                        "success": True,
                        "action": "show_product_form",
                        "prefill": prefill,
                        "answer": "Hãy điền thông tin sản phẩm vào form bên dưới nhé! 👇"
                    })
                
                # Nếu AI muốn cập nhật sản phẩm, ta cũng hiện form với thông tin cũ (trừ khi form đã được submit)
                if function_name == "update_product" and not is_form_submit:
                    product_id_query = function_args.get("product_id")
                    if product_id_query:
                        from api.models.product import Product
                        from api.models.productdetail import ProductDetail
                        from bson.errors import InvalidId
                        from mongoengine.errors import ValidationError
                        
                        product = Product.objects(name=product_id_query).first()
                        if not product:
                            try:
                                product = Product.objects(id=product_id_query).first()
                            except (InvalidId, ValidationError):
                                pass
                                
                        if product:
                            detail = ProductDetail.objects(product=product).first()
                            # Tạo prefill từ dữ liệu cũ + dữ liệu AI muốn đổi
                            prefill = {
                                "id": str(product.id),
                                "name": function_args.get("name", product.name),
                                "price": function_args.get("price", product.price),
                                "originalPrice": function_args.get("originalPrice", getattr(product, 'originalPrice', '')),
                                "category": function_args.get("category", product.category),
                                "brand": function_args.get("brand", product.brand),
                                "isNew": function_args.get("isNew", getattr(product, 'isNew', False)),
                            }
                            if detail:
                                prefill.update({
                                    "description": function_args.get("description", detail.description),
                                    "features": function_args.get("features", detail.features),
                                    "specifications": function_args.get("specifications", detail.specifications),
                                    "inStock": function_args.get("inStock", detail.inStock),
                                })
                                
                                prefill["mainImage"] = getattr(product, 'image', '')
                                prefill["galleryImages"] = getattr(detail, 'images', [])
                                
                            return JsonResponse({
                                "success": True,
                                "action": "show_product_form",
                                "prefill": prefill,
                                "answer": "Dưới đây là thông tin sản phẩm. Bạn có thể chỉnh sửa và cập nhật! 👇"
                            })
                
                # Gọi Backend Python tương ứng
                result = execute_tool_call(function_name, function_args)
                
                # Nếu action là chuyển trang, trả về luôn để frontend điều hướng UI nhanh chóng
                if function_name == "navigate_page":
                    return JsonResponse(result)
                    
                # Đưa kết quả của Backend (Tool) vào lại context của AI
                messages.append(message)
                messages.append({
                    "role": "tool",
                    "tool_call_id": tool_call.id,
                    "name": function_name,
                    "content": json.dumps(result, ensure_ascii=False)
                })
                
                # Gọi OpenAI lần 2 để AI phân tích kết quả và trả lời tự nhiên
                second_response = client.chat.completions.create(
                    model="gpt-4o-mini",
                    messages=messages,
                    max_tokens=800,
                    temperature=0.3,
                )
                
                natural_answer = second_response.choices[0].message.content
                
                return JsonResponse({
                    "success": True,
                    "action": "general_chat",
                    "answer": natural_answer
                })
            else:
                # Không gọi tool, trả lời trò chuyện thông thường
                natural_answer = message.content
                return JsonResponse({
                    "success": True,
                    "action": "general_chat",
                    "answer": natural_answer
                })
        except Exception as e:
            import traceback
            trace = traceback.format_exc()
            print(f"[AGENT ERROR] Lỗi khi gọi OpenAI API: {e}\n{trace}")
            return JsonResponse({"error": "Lỗi máy chủ Agent.", "detail": str(e), "trace": trace}, status=500)
