from astrapy import DataAPIClient
import os
from dotenv import load_dotenv

load_dotenv()

ASTRA_TOKEN = os.getenv("ASTRA_DB_APPLICATION_TOKEN")
ASTRA_API_ENDPOINT = os.getenv("ASTRA_API_ENDPOINT")

client = DataAPIClient(ASTRA_TOKEN)
db = client.get_database_by_api_endpoint(ASTRA_API_ENDPOINT)

print(f"✅ Connected to Astra DB: {db.list_collection_names()}")
