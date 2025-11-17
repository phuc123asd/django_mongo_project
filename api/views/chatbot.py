import json
from openai import OpenAI
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from api.utils.astra_client import db
from django.conf import settings
from api.json.decision import handle_admin_command
import cloudinary.uploader

client = OpenAI(api_key=settings.OPENAI_API_KEY)
collection = db.get_collection("products_embeddings")

GENERAL_CONVERSATION_PROMPT = """Bạn là một trợ lý ảo thân thiện và chuyên nghiệp cho Admin quản lý cửa hàng TechHub.
Nhiệm vụ của bạn là trả lời các câu hỏi chung của admin một cách đầy đủ và hữu ích.
Hãy giữ văn phong thân thiện, chuyên nghiệp và tự nhiên như một cuộc trò chuyện."""

@csrf_exempt
def chatbot(request):
    if request.method != "POST":
        return JsonResponse({"error": "Only POST allowed"}, status=405)

    question = ""
    role = ""
    
    if request.content_type and 'multipart/form-data' in request.content_type:
        question = request.POST.get('question', '')
        role = request.POST.get('role', '')
        
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
        except json.JSONDecodeError:
            return JsonResponse({"error": "Invalid JSON payload"}, status=400)
    if role == 'user':
        # Sinh embedding cho câu hỏi
        emb = client.embeddings.create(
            model="text-embedding-3-small",
            input=question
        ).data[0].embedding

        # Tìm 3 sản phẩm gần nhất trong Astra
        results = collection.find(
            sort={"$vector": emb},
            limit=3
        )

        context = ""
        for r in results:
            context += f"{r['name']}: {r.get('description', '')} (price: {r.get('price', 0)})\n"

        # Gửi sang GPT
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content":  "Bạn là một trợ lý ảo tư vấn sản phẩm cho TechHub. "
                    f"Dựa trên dữ liệu sản phẩm được cung cấp, hãy trả lời câu hỏi của khách hàng một cách thuyết phục. "
                    "Nếu ngữ cảnh trống, hãy trả lời dựa trên kiến thức chung và khéo léo đề nghị khách hàng liên hệ để được tư vấn. "
                    "Luôn giữ văn phong thân thiện, chuyên nghiệp."},
                {"role": "user", "content": f"Câu hỏi: {question}\nDữ liệu sản phẩm:\n{context}"}
            ],
            max_tokens=200,
        )
        answer = response.choices[0].message.content
        return JsonResponse({"answer": answer})
    else:
        command_extraction_prompt = """Bạn là một AI Agent chuyên trích xuất thông tin cho Admin quản lý cửa hàng TechHub.
        QUY TẮC BẮT BUỘC:
        1. NHIỆM VỤ CỦA BẠN LÀ PHÂN TÍCH VÀ TRÍCH XUẤT THÔNG TIN, KHÔNG PHẢI TRẢ LỜI TƯ VẤN.
        2. Ưu tiên hàng đầu là xác định đúng HÀNH ĐỘNG và tạo ra JSON tương ứng.
        3. Chỉ trả về action = "none" nếu yêu cầu hoàn toàn không liên quan đến bất kỳ hành động quản trị nào.
        4. Hãy linh hoạt với các định dạng dữ liệu. Ví dụ: "122 đô" -> price: 122, "1.jpg 2.jpg" -> images: ["1.jpg", "2.jpg"].

        CẤU TRÚC JSON TRẢ VỀ:
        {
            "action": "add_product | update_product | delete_product | reply_feedback | approve_order | reject_order | get_order_status | none",
            "payload": {
                // Thông tin trích xuất được sẽ nằm ở đây
            }
        }
        HƯỚNG DẪN CHI TIẾT CHO TỪNG HÀNH ĐỘNG:
        1.  **add_product**: Khi admin muốn thêm sản phẩm.
            - **Từ khóa**: "thêm", "tạo", "mới", "đưa vào db".
            - **NHIỆM VỤ CỦA BẠN**: Trích xuất thông tin và tạo JSON. KHÔNG trả lời câu hỏi hay yêu cầu cung cấp thêm thông tin.
            - **Trích xuất BẮT BUỘC (Phải có trong input của admin)**:
                - "name": Tên sản phẩm.
                - "price": Giá số (chỉ lấy số).
                - "images": Mảng chứa các URL đầy đủ của ảnh. Nếu admin liệt kê "https://res.cloudinary.com/dze6buir3....", hãy chuyển thành ["https://res.cloudinary.com/dze6buir..."].
            - **Suy luận TỰ ĐỘNG các trường khác (Dựa trên ngữ cảnh và tên sản phẩm)**:
                - "originalPrice": Nếu không có thông tin giảm giá, suy luận giá gốc cao hơn giá bán khoảng 10-20%. Nếu có vẻ là sản phẩm mới ra mắt không giảm giá, có thể bằng với `price` hoặc `null`.
                - "category": Xác định dựa trên tên sản phẩm gồm có("Smartphones", "Laptops", "Audio", "Smartwatches", "Tablets", "Gaming", "Drones", "Accessories").
                - "brand": Xác định dựa trên tên sản phẩm gồm có("Apple", "Samsung", "Dell", "Microsoft", "Nintendo", "DJI", "Logitech", "Canon", "GoPro", "Fitbit", "Razer", "HP", "Bose", "Google", "Asus", "Lenovo", "Xiaomi", "OnePlus", "Drones").
                - "rating": Sản phẩm cao cấp, thương hiệu lớn thường có rating cao (4.5-5.0). Sản phẩm tầm trung thấp hơn (3.5-4.5).
                - "isNew": Nếu tên sản phẩm có số phiên bản cao nhất hoặc có từ "pro", "max", "new" thì là `true`. Ngược lại là `false`.
                - "description": Viết một mô tả ngắn (1-2 câu) hấp dẫn về sản phẩm dựa trên tên và các đặc điểm đã suy luận.
                - "features": Tạo một mảng 3-5 tính năng nổi bật nhất của loại sản phẩm đó.
                - "specifications": Tạo một đối tượng chứa các thông số kỹ thuật quan trọng và phù hợp với loại sản phẩm.
                - "reviewCount": Sản phẩm mới thường có ít đánh giá (0-50). Sản phẩm phổ biến có nhiều hơn (100+).
                - "inStock": Thường là `true` trừ khi có dấu hiệu cho thấy hết hàng.
                - "hasARView": Các sản phẩm công nghệ cao, đắt tiền (đặc biệt là của Apple, Samsung) thường có tính năng này.
        2.  **update_product**: Khi admin muốn sửa thông tin sản phẩm.
            - **Từ khóa**: "sửa", "cập nhật", "đổi", "update".
            - **Trích xuất bắt buộc**:
                - "product_id": ID hoặc tên sản phẩm cần sửa.
                - "field": Trường cần sửa (ví dụ: "price", "name").
                - "value": Giá trị mới.

        3.  **delete_product**: Khi admin muốn xóa sản phẩm.
            - **Từ khóa**: "xóa", "xoá", "delete", "remove".
            - **Trích xuất bắt buộc**:
                - "product_id": ID hoặc tên sản phẩm cần xóa.

        4.  **reply_feedback**: Khi admin muốn trả lời phản hồi của khách.
            - **Từ khóa**: "trả lời", "phản hồi", "reply feedback".
            - **Trích xuất bắt buộc**:
                - "feedback_id": ID của phản hồi.
                - "reply": Nội dung trả lời.

        5.  **approve_order**: Khi admin muốn duyệt đơn hàng.
            - **Từ khóa**: "duyệt đơn", "chấp nhận đơn", "approve order".
            - **Trích xuất bắt buộc**:
                - "order_id": ID của đơn hàng.
        6.  **reject_order**: Khi admin muốn từ chối đơn hàng.
            - **Từ khóa**: "từ chối đơn", "hủy đơn", "reject order".
            - **Trích xuất bắt buộc**:
                - "order_id": ID của đơn hàng.
                - "reason": Lý do từ chối (nếu có).
        7.  **get_order_status**: Khi admin muốn kiểm tra trạng thái đơn hàng.
            - **Từ khóa**: "kiểm tra đơn", "trạng thái đơn", "order status".
            - **Trích xuất bắt buộc**:
                - "order_id": ID của đơn hàng.
        8.  **none**: Chỉ dùng khi không thể xác định được bất kỳ hành động nào ở trên.
            - **Ví dụ**: Input: "chào buổi sáng" -> Output: {"action": "none", "payload": {"reason": "unknown_command", "message": "Yêu cầu không rõ ràng."}}
        LUÔN LUÔN TRẢ VỀ MỘT ĐỐI TƯỢNG JSON HỢP LỆ, KHÔNG THÊM BẤT KỲ VĂN BẢN NÀO KHÁC.
        """
        # Gửi sang GPT
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": command_extraction_prompt},
                {"role": "user", "content": f"Câu hỏi: {question}"}
            ],
            max_tokens=500, # Tăng lên để đủ không gian cho JSON
            temperature=0,
        )
        
        answer = response.choices[0].message.content
        print(f"Phản hồi thô từ AI: {answer}")
        
        # Gọi hàm xử lý và nhận kết quả
        result = handle_admin_command(answer)

        # --- THÊM PHẦN CẢI TIẾN Ở ĐÂY ---
        if result.get("action") == "none":
            # Khi không phải lệnh admin → trả lời trò chuyện tự nhiên
            conv_response = client.chat.completions.create(
                model="gpt-4o-mini",
                messages=[
                    {"role": "system", "content": GENERAL_CONVERSATION_PROMPT},
                    {"role": "user", "content": question}
                ],
                max_tokens=250,
                temperature=0.8,
            )
            natural_answer = conv_response.choices[0].message.content
            return JsonResponse({
                "success": True,
                "action": "general_chat",
                "answer": natural_answer
            })
        return JsonResponse(result)
