from models.database_connection import get_connection


class BooksTable:
    def __init__(self):
        self.conn = get_connection()
        self.cursor = self.conn.cursor()

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        self.conn.commit()
        self.cursor.close()
        self.conn.close()

    def _create_table(self):
        self.cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS books (
                id SERIAL PRIMARY KEY,
                title TEXT NOT NULL,
                author TEXT NOT NULL,
                publisher TEXT,
                excerpt TEXT,
                sent INTEGER DEFAULT 0 CHECK (sent IN (0, 1))
            );
            """
        )

    def insert_book(self, title, author, publisher=None, excerpt=None):
        self.cursor.execute(
            """
            INSERT INTO books (title, author, publisher, excerpt, sent)
            VALUES (%s, %s, %s, %s, 0)
            """,
            (title, author, publisher, excerpt)
        )

    def get_unsent_book(self):
        self.cursor.execute(
            """
            SELECT id, title, author, publisher, excerpt
            FROM books
            WHERE sent = 0
            ORDER BY RANDOM()
            LIMIT 1
            """
        )
        result = self.cursor.fetchone()
        return {
            "id": result[0],
            "title": result[1],
            "author": result[2],
            "publisher": result[3],
            "excerpt": result[4]
        } if result else None

    def mark_book_sent(self, book_id):
        self.cursor.execute(
            "UPDATE books SET sent = 1 WHERE id = %s",
            (book_id,)
        )

    def get_sent_unsent_counts(self):
        self.cursor.execute("SELECT COUNT(*) FROM books WHERE sent = 1")
        sent_count = self.cursor.fetchone()[0]

        self.cursor.execute("SELECT COUNT(*) FROM books WHERE sent = 0")
        unsent_count = self.cursor.fetchone()[0]

        return {
            "sent": sent_count,
            "unsent": unsent_count
        }


def create_table():
    with BooksTable() as db:
        db._create_table()

def save_book(title, author, publisher=None, excerpt=None):
    with BooksTable() as db:
        db.insert_book(title, author, publisher, excerpt)

def get_unsent_book():
    with BooksTable() as db:
        return db.get_unsent_book()

def mark_book_sent(book_id):
    with BooksTable() as db:
        db.mark_book_sent(book_id)

def get_status():
    with BooksTable() as db:
        return db.get_sent_unsent_counts()
