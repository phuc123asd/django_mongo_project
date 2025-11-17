import json
from openai import OpenAI
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from api.utils.astra_client import db
from django.conf import settings
from api.json.decision import handle_admin_command

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
        
        # Trích xuất tên các file và ghép vào cuối câu hỏi
        # Ví dụ: "tôi muốn thêm iphone 17" + " 1.jpg 2.jpg" -> "tôi muốn thêm iphone 17 1.jpg 2.jpg"
        if uploaded_files:
            image_names = " " + " ".join([f.name for f in uploaded_files])
            question += image_names
            
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
            - **NHIỆM VỤ CỦA BẠN**: PHẢI trích xuất thông tin và tạo JSON. KHÔNG được trả lời câu hỏi hay yêu cầu cung cấp thêm thông tin.
            - **Trích xuất BẮT BUỘC**:
                - "name": Tên sản phẩm (ví dụ: "iphone 17").
                - "price": Giá số (chỉ lấy số, ví dụ: từ "122 đô" lấy 122).
                - "images": Mảng chứa các chuỗi ảnh. Nếu admin liệt kê "1.jpg 2.jpg 3.jpg 4.jpg", hãy chuyển thành ["1.jpg", "2.jpg", "3.jpg", "4.jpg"].
            - **Nếu THIẾU thông tin**: Vẫn tạo JSON với action "add_product". Trong payload, điền các thông tin có thể trích xuất. Các trường bắt buộc bị thiếu sẽ được xử lý bởi hệ thống. KHÔNG được báo lỗi hoặc yêu cầu thêm thông tin trong JSON này.
            - **Ví dụ trích xuất thành công**:
                - Input: "tôi muốn thêm 1 sản phẩm iphone 17 giá là 122 đô 1.jpg 2.jpg 3.jpg 4.jpg vào db"
                - Output: {"action": "add_product", "payload": {"name": "iphone 17", "price": 122, "images": ["1.jpg", "2.jpg", "3.jpg", "4.jpg"]}}
            - **Ví dụ khi THIẾU thông tin**:
                - Input: "thêm iphone 17 vào db"
                - Output: {"action": "add_product", "payload": {"name": "iphone 17", "price": null, "images": []}}

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
