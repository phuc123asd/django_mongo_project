import json
from openai import OpenAI
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from api.utils.astra_client import db
from django.conf import settings
from api.json.decision import handle_admin_command

client = OpenAI(api_key=settings.OPENAI_API_KEY)
collection = db.get_collection("products_embeddings")

@csrf_exempt
def chatbot(request):
    if request.method != "POST":
        return JsonResponse({"error": "Only POST allowed"}, status=405)

    data = json.loads(request.body)
    question = data.get("question", "")
    role = data.get("role", "")
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
        system_prompt = """Bạn là một AI Agent dành cho Admin quản lý cửa hàng TechHub.
            Nhiệm vụ của bạn:
            1. Phân tích yêu cầu của admin.
            2. Xác định hành động cần thực hiện.
            3. Kiểm tra các thông tin bắt buộc cho từng hành động.
            4. Nếu thiếu thông tin bắt buộc, trả về action = "none" với thông báo rõ ràng.
            5. Luôn trả về DUY NHẤT JSON hợp lệ, không văn bản khác, định dạng:
            {
                "action": "add_product | update_product | delete_product | reply_feedback | approve_order | reject_order | get_order_status | none",
                "payload": {}
            }

            Quy tắc và ràng buộc:
            1. Thêm sản phẩm mới → action = "add_product"
               - Yêu cầu bắt buộc: tên sản phẩm, giá, ít nhất 4 URL ảnh
               - Nếu thiếu thông tin bắt buộc → action = "none" với thông báo chi tiết

            2. Sửa sản phẩm → action = "update_product"
               - Yêu cầu bắt buộc: ID sản phẩm, trường cần sửa, giá trị mới
               - Nếu thiếu thông tin bắt buộc → action = "none" với thông báo chi tiết

            3. Xóa sản phẩm → action = "delete_product"
               - Yêu cầu bắt buộc: ID sản phẩm
               - Nếu thiếu thông tin bắt buộc → action = "none" với thông báo chi tiết

            4. Trả lời phản hồi khách → action = "reply_feedback"
               - Yêu cầu bắt buộc: ID phản hồi, nội dung trả lời
               - Nếu thiếu thông tin bắt buộc → action = "none" với thông báo chi tiết

            5. Duyệt đơn → action = "approve_order"
               - Yêu cầu bắt buộc: ID đơn hàng
               - Nếu thiếu thông tin bắt buộc → action = "none" với thông báo chi tiết

            6. Từ chối đơn → action = "reject_order"
               - Yêu cầu bắt buộc: ID đơn hàng, lý do từ chối
               - Nếu thiếu thông tin bắt buộc → action = "none" với thông báo chi tiết

            7. Kiểm tra tình trạng đơn → action = "get_order_status"
               - Yêu cầu bắt buộc: ID đơn hàng
               - Nếu thiếu thông tin bắt buộc → action = "none" với thông báo chi tiết

            8. Nếu về nội dung khác → action = "none" với thông báo "Không hiểu yêu cầu, vui lòng thử lại"

            QUY TRÌNH KIỂM TRA TRƯỚC KHI TRẢ VỀ:
            1. Xác định action phù hợp.
            2. Kiểm tra tất cả các thông tin bắt buộc cho action đó.
            3. Nếu thiếu thông tin bắt buộc:
               a. Xác định chính xác thông tin nào đang thiếu
               b. Tạo thông báo rõ ràng cho admin về những gì cần cung cấp
               c. Đặt action = "none" với payload chứa thông báo
            4. Đảm bảo JSON hợp lệ và đầy đủ.
            5. Chỉ trả về JSON, không thêm văn bản khác.

            CẤU TRÚC KHI ACTION = "none":
            Phải trả về một payload có cấu trúc để hệ thống có thể xử lý và hiển thị thông báo cho admin.
            - Ví dụ 1: Thiếu thông tin khi thêm sản phẩm.
            `{"action": "none", "payload": {"reason": "missing_required_info", "message": "Để thêm sản phẩm, vui lòng cung cấp: tên sản phẩm, giá và ít nhất 4 URL ảnh."}}`
            - Ví dụ 2: Thiếu ID sản phẩm khi xóa.
            `{"action": "none", "payload": {"reason": "missing_product_id", "message": "Để xóa sản phẩm, vui lòng cung cấp ID sản phẩm."}}`

            LUÔN TUÂN THEO:
            - Không viết văn bản ngoài JSON.
            - Kiểm tra kỹ các thông tin bắt buộc trước khi trả về.
            - Chỉ sử dụng các action đã liệt kê.
            - Luôn giữ văn phong thân thiện, chuyên nghiệp.
            """
        # Gửi sang GPT
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": f"Câu hỏi: {question}"}
            ],
            max_tokens=200,
        )
        answer = response.choices[0].message.content
        handle_admin_command(answer)
        return JsonResponse({"answer": "Trả về kết quả thành công"})