import os
import psycopg
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

def setup_database():
    db_url = os.getenv("DATABASE_URL")
    
    if not db_url:
        print("❌ Error: DATABASE_URL not found.")
        return

    print("🚀 Initializing Database Setup...")
    
    try:
        with psycopg.connect(db_url) as conn:
            with conn.cursor() as cur:
                # 1. Enable pgvector extension
                print("📦 Enabling pgvector extension...")
                cur.execute("CREATE EXTENSION IF NOT EXISTS vector;")
                
                # 2. You can add other initialization SQL here if needed
                
                conn.commit()
                print("✅ Database setup completed successfully!")

    except Exception as e:
        print(f"❌ Setup failed: {e}")

if __name__ == "__main__":
    setup_database()
