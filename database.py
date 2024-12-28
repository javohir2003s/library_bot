from dotenv import load_dotenv
import os
import psycopg2

load_dotenv()

def get_connection():
    return psycopg2.connect(
        dbname=os.getenv("NAME"),
        user=os.getenv("USER"),
        password=os.getenv("PASSWORD"),
        host=os.getenv("HOST"),
        port=os.getenv("PORT")
    )

def get_user(telegram_id):
    try:
        with get_connection() as conn:
            with conn.cursor() as cur:
                cur.execute("SELECT username FROM users WHERE telegram_id = %s", (telegram_id,))
                result = cur.fetchone()
                return result[0] if result else None
    except Exception as e:
        print(f"Xatolik yuz berdi: {e}")
        return None
    
def create_user(telegram_id: int, first_name: str | None, last_name: None, username: str | None, phone_number: str, photo_url: str | None):
    try:
        with get_connection() as conn:
            with conn.cursor() as cur:
                cur.execute("INSERT INTO users(telegram_id, first_name, last_name, phone_number,  username, photo_url) VALUES(%s, %s, %s, %s, %s, %s)", (telegram_id, first_name, last_name, phone_number, username, photo_url))
                return True
    except Exception as e:
        print(f"Xatolik yuz berdi: {e}")
        return False
