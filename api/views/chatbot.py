import json
from openai import OpenAI
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from api.utils.astra_client import db
from django.conf import settings

client = OpenAI(api_key=settings.OPENAI_API_KEY)
collection = db.get_collection("products_embeddings")

@csrf_exempt
def chatbot(request):
    if request.method != "POST":
        return JsonResponse({"error": "Only POST allowed"}, status=405)

    data = json.loads(request.body)
    question = data.get("question", "")
    
    # Phân loại đây là nhóm khách hàng hay người quản trị
    # do something
    
    
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
        max_tokens=100,
    )

    answer = response.choices[0].message.content
    return JsonResponse({"answer": answer})
