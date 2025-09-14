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
        self.cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS notes (
                id INTEGER PRIMARY KEY,
                content TEXT DEFAULT NULL,
                sent INTEGER DEFAULT 0 CHECK (sent IN (0,1))
            );
        """
        )

    def insert_note(self, note_id, content):
        self.cursor.execute(
            "INSERT INTO notes (id, content) VALUES (%s, %s)",
            (note_id, content),
        )

    def note_exists(self, note_id):
        self.cursor.execute(
            "SELECT EXISTS(SELECT 1 FROM notes WHERE id = %s)",
            (note_id,),
        )
        return self.cursor.fetchone()[0]

    def get_unsent_note(self):
        self.cursor.execute(
            "SELECT content, id FROM notes WHERE sent = 0 ORDER BY id LIMIT 1"
        )
        return self.cursor.fetchone()

    def mark_note_sent(self, note_id, content=None):
        if content:
            self.cursor.execute(
                "UPDATE notes SET sent = 1 WHERE id = %s OR content = %s",
                (note_id, content),
            )
        else:
            self.cursor.execute(
                "UPDATE notes SET sent = 1 WHERE id = %s",
                (note_id,),
            )

    def is_note_sent(self, note_id):
        self.cursor.execute(
            "SELECT sent FROM notes WHERE id = %s",
            (note_id,),
        )
        result = self.cursor.fetchone()
        return result[0] == 1 if result else False

    def update_note_content(self, note_id, content):
        self.cursor.execute(
            "UPDATE notes SET content = %s WHERE id = %s",
            (content, note_id),
        )

    def get_sent_stats(self):
        self.cursor.execute("SELECT COUNT(*) FROM notes WHERE sent = 1")
        sent = self.cursor.fetchone()[0]

        self.cursor.execute("SELECT COUNT(*) FROM notes WHERE sent = 0")
        unsent = self.cursor.fetchone()[0]

        return {"sent": sent, "unsent": unsent}


# توابع سطح بالا


def create_table():
    with NoteTableManager() as db:
        db.create_table()


def save_note(note_id, content):
    with NoteTableManager() as db:
        db.insert_note(note_id, content)


def check_is_exist(note_id):
    with NoteTableManager() as db:
        return db.note_exists(note_id)


def auto_return_content():
    with NoteTableManager() as db:
        return db.get_unsent_note()


def mark_sent(note_id=0, content=""):
    with NoteTableManager() as db:
        db.mark_note_sent(note_id, content)


def edit_content(note_id, content):
    with NoteTableManager() as db:
        db.update_note_content(note_id, content)


def get_status():
    with NoteTableManager() as db:
        return db.get_sent_stats()


def is_note_sent(note_id: int) -> bool:
    with NoteTableManager() as db:
        return db.is_note_sent(note_id)
