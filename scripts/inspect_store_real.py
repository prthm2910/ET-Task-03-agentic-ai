import os
from dotenv import load_dotenv
from langgraph.store.postgres import PostgresStore
from langchain_google_genai import GoogleGenerativeAIEmbeddings

load_dotenv()

def inspect_with_real_obj():
    embeddings = GoogleGenerativeAIEmbeddings(
        model="models/gemini-embedding-2",
        google_api_key=os.getenv("GOOGLE_API_KEY"),
        output_dimensionality=1536
    )
    
    print(f"Testing with real object: {type(embeddings)}")
    
    # Try flat
    try:
        store = PostgresStore(None, index={
            "embed": embeddings,
            "dims": 1536,
            "fields": ["fact"]
        })
        print("Flat index SUCCESS")
    except Exception as e:
        print(f"Flat index FAILED: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    inspect_with_real_obj()
