import time
import random
from datetime import datetime
import psycopg2
from faker import Faker

fake = Faker()

def get_connection():
    return psycopg2.connect(
        host="postgres_source",
        database="source_db",
        user="user",
        password="password"
    )

def insert_and_delete_article():
    conn = get_connection()
    cur = conn.cursor()
    
    # 1. Insert Artikel Baru
    title = fake.sentence(nb_words=6)
    content = fake.text(max_nb_chars=300)
    published_at = datetime.now()
    author_id = random.randint(1, 100)
    created_at = datetime.now()
    updated_at = datetime.now()
    
    insert_query = """
        INSERT INTO articles (title, content, published_at, author_id, created_at, updated_at)
        VALUES (%s, %s, %s, %s, %s, %s) RETURNING id;
    """
    cur.execute(insert_query, (title, content, published_at, author_id, created_at, updated_at))
    new_id = cur.fetchone()[0]
    conn.commit()
    print(f"[{datetime.now()}] INSERTED: Article ID {new_id}")
    
    # 2. Simulasi Hard Delete (Probabilitas 20%)
    if random.random() < 0.2:
        # Ambil ID acak untuk dihapus secara permanen
        cur.execute("SELECT id FROM articles ORDER BY RANDOM() LIMIT 1;")
        row = cur.fetchone()
        if row:
            delete_id = row[0]
            cur.execute("DELETE FROM articles WHERE id = %s;", (delete_id,))
            conn.commit()
            print(f"[{datetime.now()}] HARD DELETED: Article ID {delete_id}")

    cur.close()
    conn.close()

if __name__ == "__main__":
    print("Memulai Data Generator...")
    time.sleep(15) # Tunggu Postgres siap
    
    while True:
        try:
            insert_and_delete_article()
            time.sleep(random.randint(10, 30))
        except Exception as e:
            print(f"Error: {e}")
            time.sleep(5)