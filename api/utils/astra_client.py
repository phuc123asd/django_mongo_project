from astrapy import DataAPIClient
import os
from dotenv import load_dotenv

load_dotenv()

def _require_env(name: str) -> str:
    value = os.getenv(name)
    if not value:
        raise RuntimeError(f"Missing required environment variable: {name}")
    return value

ASTRA_TOKEN = _require_env("ASTRA_DB_APPLICATION_TOKEN")
ASTRA_API_ENDPOINT = _require_env("ASTRA_API_ENDPOINT")

client = DataAPIClient(token=ASTRA_TOKEN)
db = client.get_database_by_api_endpoint(api_endpoint=ASTRA_API_ENDPOINT)

print(f"✅ Connected to Astra DB: {db.list_collection_names()}")
