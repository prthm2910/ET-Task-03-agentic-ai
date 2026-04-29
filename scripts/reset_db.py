import os
import psycopg
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

def reset_database():
    db_url = os.getenv("DATABASE_URL")
    
    if not db_url:
        print("❌ Error: DATABASE_URL not found.")
        return

    print("🔄 Resetting Database Tables for 3072-dimension support...")
    
    try:
        with psycopg.connect(db_url) as conn:
            with conn.cursor() as cur:
                # Drop the store table (this contains the vector column with old dimensions)
                print("🗑️  Dropping table: store...")
                cur.execute("DROP TABLE IF EXISTS store CASCADE;")
                
                # Optionally drop checkpoints to start fresh
                # print("🗑️  Dropping table: checkpoints...")
                # cur.execute("DROP TABLE IF EXISTS checkpoints CASCADE;")
                
                conn.commit()
                print("✅ Database reset successfully! Tables will be recreated on next run.")

    except Exception as e:
        print(f"❌ Reset failed: {e}")

if __name__ == "__main__":
    reset_database()
