from .database_connection import get_connection

class NoteTableManager:
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
                bale_message_id BIGINT,
                eitaa_message_id BIGINT,
                sent INTEGER DEFAULT 0
            );
        """)

    def mark_sent(self, id):
        self.cursor.execute("UPDATE notes SET sent = 1 WHERE id = %s", (id,))

    def chek_id_exist(self, id):
        self.cursor.execute("SELECT id FROM notes WHERE id = %s", (id,))
        row = self.cursor.fetchone()
        return bool(row)

    def get_stats(self):
        self.cursor.execute("SELECT COUNT(*) FROM notes WHERE sent = 1")
        sent = self.cursor.fetchone()[0]
        self.cursor.execute("SELECT COUNT(*) FROM notes WHERE sent = 0")
        unsent = self.cursor.fetchone()[0]
        total = sent + unsent
        return f"📊 آمار:\n➕ کل: {total}\n✅ ارسال‌شده: {sent}\n📭 ارسال‌نشده: {unsent}"
    

    def insert_message_ids(self , id , bale_message_id , eitaa_message_id ):
        self.cursor.execute(
            'INSERT INTO notes (id , bale_message_id , eitaa_message_id) VALUES (%s,%s,%s)' ,
            (id , bale_message_id ,eitaa_message_id)
        )


def create_table_note():
    with NoteTableManager() as db:
        db.create_table()

def sent_note_message(bale_message_id):
    with NoteTableManager() as db:
        db.mark_sent(bale_message_id)

def get_note_data():
    with NoteTableManager() as db:
        return db.get_stats()
    
def save_note_ids(id , bale_id , eitaa_id):
    with NoteTableManager() as db:
        return db.insert_message_ids(id , bale_id , eitaa_id)

    