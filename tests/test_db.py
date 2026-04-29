import os

import psycopg
from dotenv import load_dotenv

# Load environment variables from .env
load_dotenv()

def test_connection():
    db_url = os.getenv("DATABASE_URL")
    
    if not db_url:
        print("❌ Error: DATABASE_URL not found in environment or .env file.")
        return

    print(f"🔄 Attempting to connect to: {db_url.split('@')[-1]}...") # Partial URL for safety
    
    try:
        # Attempt connection
        with psycopg.connect(db_url) as conn:
            with conn.cursor() as cur:
                # Run a simple query
                cur.execute("SELECT version();")
                version = cur.fetchone()
                print("✅ Connection Successful!")
                print(f"📊 PostgreSQL Version: {version[0]}")
                
                # Check for pgvector extension (required for store)
                try:
                    cur.execute("SELECT * FROM pg_extension WHERE extname = 'vector';")
                    extension = cur.fetchone()
                    if extension:
                        print("✅ pgvector extension is installed.")
                    else:
                        print("⚠️  Warning: pgvector extension is NOT installed. Long-term memory search might fail.")
                except Exception:
                    print("⚠️  Could not verify pgvector extension.")

    except Exception as e:
        print("❌ Connection Failed.")
        print(f"Internal Error: {e}")

if __name__ == "__main__":
    test_connection()
