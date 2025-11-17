import requests
from openai import OpenAI
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from api.utils.astra_client import db
from django.conf import settings

client = OpenAI(api_key=settings.OPENAI_API_KEY)
collection = db.get_collection("products_embeddings")

@csrf_exempt
def ingest_products(request):
    # Lấy dữ liệu từ API Django
    url = "http://127.0.0.1:8000/api/products/"
    products = requests.get(url).json()

    for product in products:
        text = f"{product['name']} - {product.get('description', '')}"
        emb = client.embeddings.create(
            model="text-embedding-3-small",
            input=text
        ).data[0].embedding

        # Lưu vào Astra
        collection.insert_one({
            "_id": str(product["id"]),
            "name": product["name"],
            "description": product.get("description", ""),
            "price": product.get("price", 0),
            "$vector": emb
        })

    return JsonResponse({"message": f"Indexed {len(products)} products!"})
