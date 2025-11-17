from astrapy import DataAPIClient
import os
from dotenv import load_dotenv

load_dotenv()

ASTRA_TOKEN = os.getenv("ASTRA_DB_APPLICATION_TOKEN")
ASTRA_API_ENDPOINT = os.getenv("ASTRA_API_ENDPOINT")

db = None
client = None

if ASTRA_TOKEN and ASTRA_API_ENDPOINT and ASTRA_TOKEN != "placeholder" and ASTRA_API_ENDPOINT != "placeholder":
    try:
        client = DataAPIClient(ASTRA_TOKEN)
        db = client.get_database_by_api_endpoint(ASTRA_API_ENDPOINT)
        print(f"✅ Connected to Astra DB: {db.list_collection_names()}")
    except Exception as e:
        print(f"⚠️ Warning: Could not connect to Astra DB: {e}")
        db = None
else:
    print("⚠️ Astra DB credentials not configured. Vector search will be disabled.")
