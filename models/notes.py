from models.database_connection import get_connection

class DatabaseManagerNotes:
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
            CREATE TABLE IF NOT EXISTS notes (
                id SERIAL PRIMARY KEY,
                base_message_id BIGINT,
                final_message_id BIGINT,
                sent INTEGER DEFAULT 0
            );
        """)

    def insert_base_id(self, base_id):
        self.cursor.execute(
            "INSERT INTO notes (base_message_id) VALUES (%s) RETURNING id",
            (base_id,)
        )
        return self.cursor.fetchone()[0]

    def mark_sent(self, final_id):
        self.cursor.execute(
            "UPDATE notes SET sent = 1 WHERE final_message_id = %s",
            (final_id,)
        )

    def update_final_id(self, note_id, final_id):
        self.cursor.execute(
            "UPDATE notes SET final_message_id = %s WHERE id = %s",
            (final_id, note_id)
        )

    def fetch_next_unsent(self):
        self.cursor.execute(
            "SELECT final_message_id FROM notes WHERE sent = 0 ORDER BY id LIMIT 1"
        )
        row = self.cursor.fetchone()
        return row[0] if row else None

    def fetch_by_base(self, base_id):
        self.cursor.execute(
            "SELECT final_message_id, id FROM notes WHERE base_message_id = %s",
            (base_id,)
        )
        return self.cursor.fetchone()

    def get_stats(self):
        self.cursor.execute("SELECT COUNT(*) FROM notes WHERE sent = 1 AND final_message_id IS NOT NULL")
        sent = self.cursor.fetchone()[0]
        self.cursor.execute("SELECT COUNT(*) FROM notes WHERE sent = 0 AND final_message_id IS NOT NULL")
        unsent = self.cursor.fetchone()[0]
        total = sent + unsent
        return f"📕 آمار یادداشت‌ها:\n➖ کل: {total}\n✅ ارسال‌شده: {sent}\n📭 ارسال‌نشده: {unsent}"

    def delete_base_message(self, base_id):
        self.cursor.execute(
            "DELETE FROM notes WHERE base_message_id = %s",
            (base_id,)
        )







# توابع سطح بالا
def create_table_note():
    with DatabaseManagerNotes() as db:
        db.create_table()

def save_note_id(base_id):
    with DatabaseManagerNotes() as db:
        return db.insert_base_id(base_id)

def sent_note_message(message_id):
    with DatabaseManagerNotes() as db:
        db.mark_sent(message_id)

def save_final_note_id(final_id, note_id):
    with DatabaseManagerNotes() as db:
        db.update_final_id(note_id, final_id)

def select_note():
    with DatabaseManagerNotes() as db:
        return db.fetch_next_unsent()

def select_final_note_by_base(base_id):
    with DatabaseManagerNotes() as db:
        return db.fetch_by_base(base_id)

def get_note_data():
    with DatabaseManagerNotes() as db:
        return db.get_stats()

def delete_base_note_by_id(base_id):
    with DatabaseManagerNotes() as db:
        db.delete_base_message(base_id)
