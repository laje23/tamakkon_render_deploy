# db.py
import psycopg2
import os
from dotenv import load_dotenv

load_dotenv()

def get_connection():
    try:
        return psycopg2.connect(
            dbname=os.getenv("PGDATABASE"),
            user=os.getenv("PGUSER"),
            password=os.getenv("PGPASSWORD"),
            host=os.getenv("PGHOST"),
            port=os.getenv("PGPORT")
        )
    except psycopg2.Error as e:
        print("⚠️ اتصال به دیتابیس ناموفق بود:", e)
        return None
