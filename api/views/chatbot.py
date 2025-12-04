import json
from openai import OpenAI
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from api.utils.astra_client import db
from django.conf import settings
from api.json.decision import handle_admin_command
from api.json.prompt import *
import cloudinary.uploader

client = OpenAI(api_key=settings.OPENAI_API_KEY)
collection = db.get_collection("products_embeddings")

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
                {"role": "system", "content":  GENERAL_TELESELF_PROMPT},
                {"role": "user", "content": f"Câu hỏi: {question}\nDữ liệu sản phẩm:\n{context}"}
            ],
            max_tokens=200,
        )
        answer = response.choices[0].message.content
        return JsonResponse({"answer": answer})
    else:
        # Gửi sang GPT
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": command_extraction_prompt},
                {"role": "user", "content": f"Câu hỏi: {question}"}
            ],
            max_tokens=500,
            temperature=0,
        )
        
        answer = response.choices[0].message.content
        print(f"Phản hồi thô từ AI: {answer}")
        
        # Gọi hàm xử lý và nhận kết quả
        result = handle_admin_command(answer)

        
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
        elif result.get("action") == "statistics":
            try:
                stats_data = result.get("message", {})
                
                # Tạo một prompt để GPT diễn giải dữ liệu thống kê thành văn bản tự nhiên
                analyst_prompt = f"""
                Bạn là một nhà phân tích kinh doanh chuyên nghiệp cho cửa hàng TechHub.
                Dựa trên dữ liệu thống kê được cung cấp dưới dạng JSON, hãy tạo một bản tóm tắt ngắn gọn, súc tích và hấp dẫn cho quản trị viên.
                Bản tóm tắt nên làm nổi bật các điểm chính, các xu hướng quan trọng và những hiểu biết có giá trị.
                Hãy trình bày một cách rõ ràng và dễ hiểu.
                Dữ liệu thống kê:
                {json.dumps(stats_data, indent=2, ensure_ascii=False)}
                """
                
                # Gọi API OpenAI để tạo bản tóm tắt
                conv_response = client.chat.completions.create(
                    model="gpt-4o-mini",
                    messages=[
                        {"role": "system", "content": analyst_prompt},
                    ],
                     max_tokens=500,
                    temperature=0.7,              
                )
                
                natural_summary = conv_response.choices[0].message.content.strip()
                
                # Trả về kết quả với định dạng chuẩn
                return JsonResponse({
                    "success": True,
                    "action": "statistics",
                    "answer": natural_summary
                })
            except Exception as e:
                print(f"[CHATBOT] Lỗi khi tóm tắt thống kê: {e}")
                return JsonResponse({
                    "success": False,
                    "action": "statistics",
                    "error": f"Không thể tạo tóm tắt: {str(e)}",
                    # Bạn có thể chọn trả về dữ liệu thô để gỡ lỗi
                    "raw_data": result.get("message", {}) 
                }, status=500) # Trả về mã lỗi 500 cho lỗi máy chủ
        return JsonResponse(result)
