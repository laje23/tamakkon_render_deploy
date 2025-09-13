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

    def insert_content_and_id(self, content, id):
        self.cursor.execute(
            "INSERT INTO notes (id, content) VALUES (%s, %s)",
            (id, content),
        )

    def check_id_exist(self, id):
        self.cursor.execute(
            "SELECT EXISTS(SELECT 1 FROM notes WHERE id = %s)",
            (id,),
        )
        return self.cursor.fetchone()[0]

    def return_auto_content(self):
        self.cursor.execute(
            "SELECT content, id FROM notes WHERE sent = 0 ORDER BY id LIMIT 1"
        )
        return self.cursor.fetchone()

    def update_sent_to_1(self, id, content=None):
        if content:
            self.cursor.execute(
                "UPDATE notes SET sent = 1 WHERE id = %s OR content = %s",
                (id, content),
            )
        else:
            self.cursor.execute(
                "UPDATE notes SET sent = 1 WHERE id = %s",
                (id,),
            )

    def count_sent_status(self):
        self.cursor.execute(
            "SELECT COUNT(*) FROM notes WHERE sent = 1"
        )
        sent_count = self.cursor.fetchone()[0]

        self.cursor.execute(
            "SELECT COUNT(*) FROM notes WHERE sent = 0"
        )
        unsent_count = self.cursor.fetchone()[0]

        return {
            "sent": sent_count,
            "unsent": unsent_count
        }
    
    def return_sent(self, id):
        self.cursor.execute(
            "SELECT sent FROM notes WHERE id = %s",
            (id,),
        )
        result = self.cursor.fetchone()
        return result[0] if result else None

    def update_content(self, id, content):
        self.cursor.execute(
            "UPDATE notes SET content = %s WHERE id = %s",
            (content, id),
        )


# توابع بیرون کلاس

def create_table():
    with NoteTableManager() as db:
        db.create_table()


def save_note(id, content):
    with NoteTableManager() as db:
        db.insert_content_and_id(content, id)


def check_is_exist(id):
    with NoteTableManager() as db:
        return db.check_id_exist(id)


def auto_return_content():
    with NoteTableManager() as db:
        return db.return_auto_content()


def mark_sent(id=0, content=""):
    with NoteTableManager() as db:
        db.update_sent_to_1(id, content)

def return_sent(id):
    with NoteTableManager() as db:
        return db.return_sent(id)


def edit_content(id, content):
    with NoteTableManager() as db:
        db.update_content(id, content)


def get_status():
    with NoteTableManager() as db:
        return db.count_sent_status()
