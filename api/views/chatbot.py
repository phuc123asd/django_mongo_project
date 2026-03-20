import json
from openai import OpenAI
from typing import Any, cast
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.conf import settings
from api.json.decision import handle_admin_command, execute_tool_call
from api.json.prompt import GENERAL_CONVERSATION_PROMPT, GENERAL_TELESELF_PROMPT, command_extraction_prompt
import cloudinary.uploader
from api.utils.openai_tools import ADMIN_TOOLS
import re
from api.models.product import Product
from api.models.productdetail import ProductDetail
from api.models.order import Order
from mongoengine import Q
from mongoengine.errors import ValidationError
from bson.errors import InvalidId

client = OpenAI(api_key=settings.OPENAI_API_KEY)

def _objects(model: Any) -> Any:
    return model.objects

@csrf_exempt
def chatbot(request):
    if request.method != "POST":
        return JsonResponse({"error": "Only POST allowed"}, status=405)

    question = ""
    role = ""
    is_form_submit = False
    form_payload = None
    uploaded_image_urls = []
    
    if request.content_type and 'multipart/form-data' in request.content_type:
        print(f"[CHATBOT] Xử lý request dạng multipart/form-data")
        question = request.POST.get('question', '')
        role = request.POST.get('role', '')
        is_form_submit = request.POST.get('is_form_submit', 'false') == 'true'
        form_payload_raw = request.POST.get('form_payload', '')
        if form_payload_raw:
            try:
                parsed_payload = json.loads(form_payload_raw)
                if isinstance(parsed_payload, dict):
                    form_payload = parsed_payload
            except Exception:
                form_payload = None
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
                    uploaded_image_urls.append(image_url)
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
            raw_payload = data.get("form_payload")
            if isinstance(raw_payload, dict):
                form_payload = raw_payload
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
        keyword_content = keyword_response.choices[0].message.content
        keyword = keyword_content.strip() if keyword_content else ""

        # Tìm kiếm bằng MongoEngine với phân biệt chữ hoa/thường (icontains)
        
        # Tìm các sản phẩm có contains trong tên hoặc danh mục
        results = _objects(Product)(
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
        if is_form_submit and isinstance(form_payload, dict):
            action = form_payload.get("action")
            payload = form_payload.get("payload", {})
            if not action or not isinstance(payload, dict):
                return JsonResponse(
                    {"success": False, "error": "Dữ liệu form_payload không hợp lệ."},
                    status=400
                )

            # Ưu tiên payload có cấu trúc từ form.
            # - add_product: dùng images như cũ
            # - update_product: tách mainImage (Product.image) và galleryImages (ProductDetail.images)
            if action == "update_product":
                existing_gallery = payload.get("galleryImages", [])
                if not isinstance(existing_gallery, list):
                    existing_gallery = []
                remaining_uploaded_urls = list(uploaded_image_urls)

                if payload.get("mainImageUpload"):
                    if remaining_uploaded_urls:
                        payload["mainImage"] = remaining_uploaded_urls[0]
                        remaining_uploaded_urls = remaining_uploaded_urls[1:]
                    payload.pop("mainImageUpload", None)

                combined_gallery = [*existing_gallery, *remaining_uploaded_urls]
                payload["galleryImages"] = combined_gallery
            else:
                existing_images = payload.get("images", [])
                if not isinstance(existing_images, list):
                    existing_images = []
                combined_images = [*existing_images, *uploaded_image_urls]
                if combined_images:
                    payload["images"] = combined_images

            result = execute_tool_call(action, payload)
            return JsonResponse(result)
        
        system_prompt = (
            "Bạn là AI Agent Admin thông minh quản lý cửa hàng TechHub. "
            "Nhiệm vụ của bạn là gọi các Func/Tools phù hợp theo yêu cầu của người dùng, hoặc trả lời tự nhiên nếu không có tool thích hợp. "
            "Khi sử dụng tool, luôn trả về tham số đúng định dạng JSON yêu cầu. "
            "ĐẶC BIỆT: Phân biệt rõ 'Tính năng nổi bật' (features: mảng các chuỗi, VD: ['Màn hình OLED', 'Pin 5000mAh']) "
            "và 'Thông số kỹ thuật' (specifications: object key-value, VD: {'Chip': 'A18', 'RAM': '8GB'}). "
            "Khi thấy người dùng yêu cầu 'mở trang', 'chuyển đến', 'đi tới', hãy sử dụng tool navigate_page. "
            "QUAN TRỌNG: Khi người dùng muốn thêm/tạo sản phẩm mới (dù chưa cung cấp đủ thông tin), "
            "hãy GỌI NGAY tool add_product với những thông tin có sẵn. Nếu không biết tên sản phẩm, hãy truyền name='Sản phẩm mới' để kích hoạt form. "
            "TUYỆT ĐỐI KHÔNG hỏi lại hay liệt kê yêu cầu — hệ thống sẽ tự hiện form để admin điền còn lại. "
            "QUAN TRỌNG: Khi người dùng muốn SỬA/CẬP NHẬT/CHỈNH SỬA sản phẩm (dù chỉ cung cấp ID hoặc tên), "
            "hãy GỌI NGAY tool update_product với product_id tương ứng. "
            "KHÔNG hỏi lại 'bạn muốn sửa gì' — hệ thống sẽ tự hiện form chứa dữ liệu hiện tại để admin chỉnh sửa. "
            "QUAN TRỌNG: Khi người dùng muốn DUYỆT đơn hàng, hãy GỌI NGAY tool approve_order. "
            "Nếu họ nói 'duyệt tất cả' hoặc không chỉ rõ ID, truyền order_ids=[]. "
            "Nếu nói 'duyệt N đơn mới nhất', cũng truyền order_ids=[] — hệ thống sẽ xử lý. "
            "KHÔNG hỏi lại — hệ thống sẽ hiện danh sách đơn hàng để admin xác nhận trước khi duyệt."
        )
        
        if "biểu đồ" in question.lower() or "chart" in question.lower() or "vẽ" in question.lower():
            system_prompt += (
                "\n\n[QUAN TRỌNG NHẤT]: Người dùng yêu cầu VẼ BIỂU ĐỒ. Bạn BẮT BUỘC phải làm theo trình tự sau:\n"
                "1. Gọi Tool `get_statistics` để lấy số liệu thực tế.\n"
                "2. Khi nhận được kết quả thống kê, hãy tìm mảng `chart_data` trong kết quả đó.\n"
                "3. BẠN PHẢI LẬP TỨC gọi Tool `draw_chart` để vẽ biểu đồ.\n"
                "4. CHÚ Ý: Bạn BẮT BUỘC phải truyền mảng `chart_data` vừa lấy được vào tham số `data` của hàm `draw_chart`. KHÔNG ĐƯỢC BỎ QUÊN tham số `data` này!\n"
                "5. TUYỆT ĐỐI KHÔNG trả lời bằng văn bản (text) thay vì vẽ biểu đồ!"
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
            # Cho phép AI suy luận qua nhiều bước (hỗ trợ gọi tool liên tiếp)
            MAX_STEPS = 5
            for step in range(MAX_STEPS):
                response = client.chat.completions.create(
                    model="gpt-4o", # Model mạnh hơn xíu để xử lý chain lý luận
                    messages=messages,
                    tools=cast(Any, ADMIN_TOOLS),
                    tool_choice="auto",
                    parallel_tool_calls=False,
                    max_tokens=800,
                    temperature=0.2,
                )
                
                message = response.choices[0].message
                
                # Nếu AI trả về function call
                tool_calls = getattr(message, "tool_calls", None)
                if tool_calls:
                    messages.append(message)
                    tool_call: Any = tool_calls[0]
                    function_obj: Any = getattr(tool_call, "function", None)
                    function_name = getattr(function_obj, "name", "")
                    function_arguments = getattr(function_obj, "arguments", "{}")
                    
                    try:
                        function_args = json.loads(function_arguments)
                    except Exception as e:
                        function_args = {}
                        print(f"[TOOL PARSE ERROR] Lỗi phân tích JSON Argument: {e}")

                    print(f"[AGENT ACTIVATED] Bước {step+1}: AI Gọi {function_name} | Tham số: {function_args}")
                    
                    # Render frontend form nếu AI muốn add data
                    if function_name == "add_product" and not function_args.get("images") and not is_form_submit:
                        prefill = {k: v for k, v in function_args.items() if k != "images"}
                        return JsonResponse({
                            "success": True,
                            "action": "show_product_form",
                            "prefill": prefill,
                            "answer": "Hãy điền thông tin sản phẩm vào form bên dưới nhé! 👇"
                        })
                    
                    # Render frontend form nếu AI muốn update data
                    if function_name == "update_product" and not is_form_submit:
                        product_id_query = function_args.get("product_id")
                        if product_id_query:
                            
                            product = _objects(Product)(name=product_id_query).first()
                            if not product:
                                try:
                                    product = _objects(Product)(id=product_id_query).first()
                                except (InvalidId, ValidationError):
                                    pass
                                    
                            if product:
                                detail = _objects(ProductDetail)(product=product).first()
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
                    
                    # Render frontend card nếu AI muốn duyệt đơn hàng
                    if function_name == "approve_order" and not is_form_submit:
                        
                        order_ids = function_args.get("order_ids", [])
                        
                        if not order_ids:
                            orders = _objects(Order)(status='Đang Xử Lý').order_by('-created_at').limit(20)
                        else:
                            orders = []
                            for oid in order_ids:
                                try:
                                    o = _objects(Order)(id=oid).first()
                                    if o:
                                        orders.append(o)
                                except (InvalidId, Exception):
                                    pass
                        
                        if not orders:
                            # Không có đơn nào → trả text bình thường
                            messages.append({
                                "role": "tool",
                                "tool_call_id": tool_call.id,
                                "name": function_name,
                                "content": json.dumps({"success": False, "error": "Không có đơn hàng nào đang chờ duyệt."}, ensure_ascii=False)
                            })
                            continue
                        
                        order_list = []
                        for o in orders:
                            customer_name = "Không rõ"
                            if o.customer:
                                try:
                                    customer_name = f"{o.customer.first_name} {o.customer.last_name}"
                                except Exception:
                                    pass
                            
                            # Resolve product names
                            items_data = []
                            for item in (o.items or []):
                                product_name = "Sản phẩm"
                                if item.product_id:
                                    try:
                                        p = _objects(Product)(id=item.product_id).first()
                                        if p:
                                            product_name = p.name
                                    except Exception:
                                        pass
                                items_data.append({
                                    "productName": product_name,
                                    "quantity": item.quantity,
                                    "unitPrice": str(item.unit_price) if item.unit_price else "0",
                                })
                            
                            order_list.append({
                                "id": str(o.id),
                                "customerName": customer_name,
                                "phone": o.phone or "",
                                "shippingAddress": f"{o.shipping_address}, {o.city}, {o.province}",
                                "paymentMethod": o.payment_method or "cod",
                                "paymentStatus": o.payment_status or "pending",
                                "totalPrice": str(o.total_price),
                                "status": o.status,
                                "items": items_data,
                                "createdAt": o.created_at.strftime("%d/%m/%Y %H:%M") if o.created_at else "",
                            })
                        
                        return JsonResponse({
                            "success": True,
                            "action": "show_order_approval",
                            "orders": order_list,
                            "answer": f"Có {len(order_list)} đơn hàng đang chờ duyệt. Vui lòng kiểm tra và xác nhận! 👇"
                        })

                    # Gọi Backend Python Tool
                    result = execute_tool_call(function_name, function_args)
                    
                    # Nếu action là draw_chart hoặc navigate_page -> ngắt vòng lặp, trả về luôn giao diện
                    if function_name in ["navigate_page", "draw_chart"]:
                        # TỰ ĐỘNG CHÈN DỮ LIỆU NẾU AI QUÊN TRUYỀN `data` CHO BIỂU ĐỒ
                        if function_name == "draw_chart" and not result.get("data"):
                            import json as jsn
                            print("\n[INJECT] AI did not provide 'data', searching history for 'get_statistics'...")
                            for past_msg in reversed(messages):
                                if isinstance(past_msg, dict) and past_msg.get("role") == "tool" and past_msg.get("name") == "get_statistics":
                                    print("[INJECT] Found previous 'get_statistics' result in messages!")
                                    try:
                                        stats_data = jsn.loads(past_msg.get("content", "{}"))
                                        if "raw_data" in stats_data and "chart_data" in stats_data["raw_data"]:
                                            result["data"] = stats_data["raw_data"]["chart_data"]
                                            print(f"[INJECT] Successfully injected {len(result['data'])} rows into chart payload!")
                                            break
                                        else:
                                            print("[INJECT] 'chart_data' not found in raw_data!")
                                            print("Raw keys:", stats_data.get("raw_data", {}).keys())
                                    except Exception as e:
                                        print(f"[INJECT ERROR] {e}")
                                        pass

                        return JsonResponse(result)
                        
                    # Mấu chốt: Thêm kết quả của Tool vào để AI tiếp tục vòng lặp suy luận
                    messages.append({
                        "role": "tool",
                        "tool_call_id": tool_call.id,
                        "name": function_name,
                        "content": json.dumps(result, ensure_ascii=False)
                    })
                    print(f"[AGENT THOUGHT] Đã gửi kết quả {function_name} lại cho AI...")
                else:
                    # Kết thúc vòng lặp (AI không gọi Tool nữa, chỉ chat tự nhiên)
                    return JsonResponse({
                        "success": True,
                        "action": "general_chat",
                        "answer": message.content or "Đã thực hiện xong yêu cầu."
                    })
            
            # Nếu vòng lặp chạy quá số lần giới hạn
            return JsonResponse({
                "success": True,
                "action": "general_chat",
                "answer": "Yêu cầu có quá nhiều bước lấy dữ liệu. Hãy thử chia nhỏ câu hỏi nhé!"
            })
        except Exception as e:
            import traceback
            trace = traceback.format_exc()
            print(f"[AGENT ERROR] Lỗi khi gọi OpenAI API: {e}\n{trace}")
            return JsonResponse({"error": "Lỗi máy chủ Agent.", "detail": str(e), "trace": trace}, status=500)
