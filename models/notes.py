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
                id INTEGER PRIMARY KEY,
                message_id BIGINT,
                sent INTEGER DEFAULT 0
            );
        """)

    def save_notes(self , message_id , id):
        self.cursor.execute('INSERT INTO notes (id) , (message_id) VALUES (%s,%s)' , (id , message_id))

    def mark_sent(self, final_id):
        self.cursor.execute(
            "UPDATE notes SET sent = 1 WHERE message_id = %s",
            (final_id,)
        )

    def get_stats(self):
        self.cursor.execute("SELECT COUNT(*) FROM notes WHERE sent = 1 AND message_id IS NOT NULL")
        sent = self.cursor.fetchone()[0]
        self.cursor.execute("SELECT COUNT(*) FROM notes WHERE sent = 0 AND message_id IS NOT NULL")
        unsent = self.cursor.fetchone()[0]
        total = sent + unsent
        return f"📕 آمار یادداشت‌ها:\n➖ کل: {total}\n✅ ارسال‌شده: {sent}\n📭 ارسال‌نشده: {unsent}"





# توابع سطح بالا
def create_table_note():
    with DatabaseManagerNotes() as db:
        db.create_table()

def sent_note_message(message_id):
    with DatabaseManagerNotes() as db:
        db.mark_sent(message_id)

def get_note_data():
    with DatabaseManagerNotes() as db:
        return db.get_stats()
def save_note(id , message_id):
    with DatabaseManagerNotes() as db:
        db.save_notes(message_id , id)

