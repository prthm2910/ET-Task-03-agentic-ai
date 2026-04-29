import os
import sys
from dotenv import load_dotenv

# Add src to path
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
sys.path.insert(0, project_root)

load_dotenv()

from src.services.embeddings import get_embeddings_provider
from src.core.config import settings

def debug():
    print(f"Embedding model: {settings.embedding_model}")
    print(f"Google API Key length: {len(settings.google_api_key) if settings.google_api_key else 0}")
    
    embed = get_embeddings_provider()
    print(f"Embed provider: {embed}")
    
    if embed is None:
        print("FAILED: Embed provider is None")
    else:
        print("SUCCESS: Embed provider created")

if __name__ == "__main__":
    debug()
