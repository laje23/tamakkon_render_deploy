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

    def save_notes(self, message_id, id):
        self.cursor.execute(
            'INSERT INTO notes (id, message_id) VALUES (%s, %s)',
            (id, message_id))


    def mark_sent(self, final_id):
        self.cursor.execute(
            "UPDATE notes SET sent = 1 WHERE message_id = %s",
            (final_id,)
        )

    def chek_id_exist(self , id ):
        self.cursor.execute('SELECT id FROM notes WHERE id = %s ' ,(id,) )
        _id = self.cursor.fetchone()
        return _id[0] if _id else None

    def select_messageid_by_id(self , id):
        self.cursor.execute('SELECT message_id FROM notes WHERE id = %s ', (id,))
        _id = self.cursor.fetchone()
        return _id[0] if _id else None

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

def chek_id_is_exist(id) -> bool:
    with DatabaseManagerNotes() as db:
        is_exist = db.chek_id_exist(id)
        if is_exist:
            return True
        return False

def select_message_id_by_id(id):
    with DatabaseManagerNotes() as db:
        x = db.select_messageid_by_id(id)
        return x if x else None