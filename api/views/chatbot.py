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
            "action": "add_product | update_product | delete_product | approve_order | none",
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
                - "isNew": Nếu tên sản phẩm có số phiên bản cao nhất, "new" thì là `true`. Ngược lại là `false`.
                - "description": VIẾT MÔ TẢ HẤP DẪN và lôi cuốn:
                    * Bắt đầu bằng một câu khẳng định mạnh mẽ về sản phẩm
                    * Tập trung vào lợi ích thực tế cho người dùng, không chỉ tính năng
                    * Sử dụng từ ngữ gợi cảm xúc (đột phá, tuyệt vời, không thể bỏ qua, etc.)
                    * Kết thúc bằng lời kêu gọi hành động hoặc lời khuyên hữu ích
                    * Ví dụ: "Trải nghiệm công nghệ đỉnh cao với iPhone 15 Pro - thiết kế titan siêu bền, chip A17 Pro mạnh mẽ hơn 30% và camera zoom quang học 5x không đối thủ. Nâng cấp ngay hôm nay để khám phá tiềm năng không giới hạn!"
                - "features": Tạo một mảng 3-5 tính năng nổi bật nhất:
                    * Mỗi tính năng nên bắt đầu bằng động từ mạnh (Tận hưởng, Khám phá, Trải nghiệm, etc.)
                    * Tập trung vào lợi ích trực tiếp cho người dùng
                    * Sử dụng ngôn ngữ gợi hình và hấp dẫn
                    * Ví dụ: ["Tận hưởng màn hình Super Retina XDR với độ sáng vượt trội", "Khám phá sức mạnh của chip A17 Pro với hiệu năng đột phá", "Chụp ảnh chuyên nghiệp với hệ thống 3 camera và zoom quang học 5x"]
                - "specifications": Tạo đối tượng thông số kỹ thuật ấn tượng:
                    * Sử dụng thuật ngữ chuyên ngành phù hợp
                    * Làm nổi bật các thông số quan trọng nhất
                    * Thêm đơn vị đo lường để tăng độ tin cậy
                    * Ví dụ: {"Màn hình": "6.1 inch Super Retina XDR", "Chip": "A17 Pro 6 nhân", "Camera": "48MP chính + 12MP siêu rộng + 12MP tele", "Pin": "Lên đến 23 giờ video playback", "Bộ nhớ": "128GB/256GB/512GB/1TB", "Kháng nước": "IP68"}
                - "reviewCount": Sản phẩm mới thường có ít đánh giá (0-50). Sản phẩm phổ biến có nhiều hơn (100+).
                - "inStock": Thường là `true` trừ khi có dấu hiệu cho thấy hết hàng.
                - "hasARView": Các sản phẩm công nghệ cao, đắt tiền (đặc biệt là của Apple, Samsung) thường có tính năng này.
        2. **update_product**: Khi admin muốn CẬP NHẬT hoặc THAY ĐỔI thông tin sản phẩm.
            - **Từ khóa**: "sửa", "cập nhật", "đổi", "update", "thay đổi", "chỉnh sửa", "sửa lại", "cập nhật lại", "đổi thành", "thiết lập lại", "giảm giá", "tăng giá".
            
            - **Trích xuất BẮT BUỘC**:
                - "product_id": Tên hoặc ID của sản phẩm cần cập nhật.
                - **ÍT NHẤT MỘT TRONG CÁC TRƯỜNG DƯỚI ĐÂY**:
                    - "name": Tên mới của sản phẩm
                    - "price": Giá mới
                    - "originalPrice": Giá gốc mới
                    - "image": URL ảnh chính mới
                    - "images": Mảng URL ảnh mới
                    - "category": Danh mục mới
                    - "brand": Thương hiệu mới
                    - "rating": Đánh giá mới
                    - "isNew": Trạng thái mới (true/false)
                    - "description": Mô tả mới
                    - "features": Mảng tính năng mới
                    - "specifications": Đối tượng thông số kỹ thuật mới
                    - "inStock": Trạng thái tồn kho (true/false)
                    - "hasARView": Tính năng AR (true/false)
                    - "reviewCount": Số lượng đánh giá mới
            
            - **VÍ DỤ CỤ THỂ**:
                - Input: "Sửa giá iPhone 15 Pro thành 1200"
                - Output: {"action": "update_product", "payload": {"product_id": "iPhone 15 Pro", "price": 1200}}
                
                - Input: "Cập nhật lại giá gốc của Samsung Galaxy S24 thành 1400 và giá bán là 1200"
                - Output: {"action": "update_product", "payload": {"product_id": "Samsung Galaxy S24", "originalPrice": 1400, "price": 1200}}
                
                - Input: "Đổi tên Dell XPS 13 thành Dell XPS 13 Plus và cập nhật mô tả là 'Laptop ultrabook mạnh mẽ'"
                - Output: {"action": "update_product", "payload": {"product_id": "Dell XPS 13", "name": "Dell XPS 13 Plus", "description": "Laptop ultrabook mạnh mẽ"}}
                
                - Input: "Giảm giá iPad Air xuống 500 và đánh giá 4.8 sao"
                - Output: {"action": "update_product", "payload": {"product_id": "iPad Air", "price": 500, "rating": 4.8}}
                
                - Input: "Cập nhật thông số kỹ thuật cho Sony WH-1000XM5: pin 30 giờ, chống ồn ANC"
                - Output: {"action": "update_product", "payload": {"product_id": "Sony WH-1000XM5", "specifications": {"pin": "30 giờ", "chống_ồn": "ANC"}}}
                
                - Input: "Thêm ảnh mới cho MacBook Pro: https://example.com/img1.jpg, https://example.com/img2.jpg"
                - Output: {"action": "update_product", "payload": {"product_id": "MacBook Pro", "images": ["https://example.com/img1.jpg", "https://example.com/img2.jpg"]}}
                
                - Input: "Đánh dấu iPhone 14 là không còn hàng"
                - Output: {"action": "update_product", "payload": {"product_id": "iPhone 14", "inStock": false}}
                
                - Input: "Cập nhật tính năng cho Apple Watch Series 9: ['Theo dõi oxy máu', 'GPS', 'Chống nước 50m']"
                - Output: {"action": "update_product", "payload": {"product_id": "Apple Watch Series 9", "features": ["Theo dõi oxy máu", "GPS", "Chống nước 50m"]}}
            
            - **LƯU Ý QUAN TRỌNG**:
                - Luôn xác định đúng sản phẩm cần cập nhật dựa trên tên hoặc ID
                - Có thể cập nhật nhiều trường cùng lúc
                - Nếu admin nói "giảm giá" hoặc "tăng giá" mà không nói giá cụ thể, hãy hỏi giá mới
                - Với thông số kỹ thuật, tạo đối tượng với các cặp key-value phù hợp

        3.  **delete_product**: Khi admin muốn xóa sản phẩm.
            - **Từ khóa**: "xóa", "delete", "remove".
            - **Trích xuất bắt buộc**:
                - "product_id": ID (Nếu thiếu thì yêu cầu người dung bổ sung)

        4.  **approve_order**: Khi admin muốn duyệt đơn hàng.
            - **Từ khóa**: "duyệt đơn", "chấp nhận đơn", "approve order", "duyệt nhiều đơn", "duyệt tất cả đơn".
            - **Trích xuất bắt buộc**:
                - "order_ids": Mảng chứa các ID của đơn hàng cần duyệt. Nếu admin nói "duyệt tất cả", hãy đặt mảng này là rỗng [].
            
            - **VÍ DỤ CỤ THỂ**:
                - Input: "Duyệt đơn 12345"
                - Output: {"action": "approve_order", "payload": {"order_ids": ["12345"]}}
                
                - Input: "Duyệt các đơn 12345, 67890, 54321"
                - Output: {"action": "approve_order", "payload": {"order_ids": ["12345", "67890", "54321"]}}
                
                - Input: "Duyệt tất cả đơn hàng đang chờ"
                - Output: {"action": "approve_order", "payload": {"order_ids": []}}
        5.  **none**: Chỉ dùng khi không thể xác định được bất kỳ hành động nào ở trên.
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
