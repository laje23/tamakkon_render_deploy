from models.database_connection import get_connection

class DatabaseManagerHadith:
    def __init__(self):
        self.conn = get_connection()
        self.cursor = self.conn.cursor()

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        self.conn.commit()
        self.cursor.close()
        self.conn.close()

    def create_table(self):
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS hadith (
                id SERIAL PRIMARY KEY,
                base_message_id BIGINT,
                final_message_id BIGINT,
                sent INTEGER DEFAULT 0
            );
        """)

    def insert_base_id(self, base_id):
        self.cursor.execute(
            "INSERT INTO hadith (base_message_id) VALUES (%s) RETURNING id",
            (base_id,)
        )
        return self.cursor.fetchone()[0]

    def fetch_random_unsent(self):
        self.cursor.execute(
            "SELECT final_message_id FROM hadith WHERE sent = %s ORDER BY RANDOM() LIMIT 1"
        , (0,))
        row = self.cursor.fetchone()
        return row[0] if row else None

    def fetch_by_id(self, id):
        self.cursor.execute(
            "SELECT final_message_id, sent FROM hadith WHERE id = %s",
            (id,)
        )
        return self.cursor.fetchone()

    def update_final_id(self, final_id, id):
        self.cursor.execute(
            "UPDATE hadith SET final_message_id = %s WHERE id = %s",
            (final_id, id)
        )

    def mark_sent(self, message_id):
        self.cursor.execute(
            "UPDATE hadith SET sent = 1 WHERE final_message_id = %s",
            (message_id,)
        )

    def get_by_base(self, base_id):
        self.cursor.execute(
            "SELECT final_message_id, id FROM hadith WHERE base_message_id = %s",
            (base_id,)
        )
        return self.cursor.fetchone()

    def get_stats(self):
        self.cursor.execute("SELECT COUNT(*) FROM hadith WHERE sent = 1 AND final_message_id IS NOT NULL")
        sent = self.cursor.fetchone()[0]
        self.cursor.execute("SELECT COUNT(*) FROM hadith WHERE sent = 0 AND final_message_id IS NOT NULL")
        unsent = self.cursor.fetchone()[0]
        total = sent + unsent
        return f"📗 آمار احادیث:\n➖ کل: {total}\n✅ ارسال‌شده: {sent}\n📭 ارسال‌نشده: {unsent}"


    def get_base_ids_without_final(self):
        self.cursor.execute("SELECT base_message_id FROM hadith WHERE final_message_id IS NULL")
        rows = self.cursor.fetchall()
        return [row[0] for row in rows]



    def delete_base_message(self , id):
        self.cursor.execute('DELETE FROM hadiths WHERE base_message_id = %s' , (id,))

# توابع سطح بالا
def create_hadith_table():
    with DatabaseManagerHadith() as db:
        db.create_table()

def save_base_hadith_id(base_id):
    with DatabaseManagerHadith() as db:
        return db.insert_base_id(base_id)

def select_random_hadith():
    with DatabaseManagerHadith() as db:
        return db.fetch_random_unsent()

def select_hadith_by_id(id):
    with DatabaseManagerHadith() as db:
        return db.fetch_by_id(id)

def save_final_hadith_id(final_id, hadith_id):
    with DatabaseManagerHadith() as db:
        db.update_final_id(final_id, hadith_id)

def sent_message(message_id):
    with DatabaseManagerHadith() as db:
        db.mark_sent(message_id)

def select_finalid_by_baseid(base_id):
    with DatabaseManagerHadith() as db:
        return db.get_by_base(base_id)

def get_hadith_data():
    with DatabaseManagerHadith() as db:
        return db.get_stats()

def fetch_base_ids_without_final():
    with DatabaseManagerHadith() as db:
        return db.get_base_ids_without_final()
    
def delete_base_hadith_by_id(base_id):
    with DatabaseManagerHadith() as db:
        db.delete_base_message(base_id)

    
    
    
