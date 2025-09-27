from models.database_connection import get_connection


class MediaTableManager:
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
            CREATE TABLE IF NOT EXISTS media (
                id SERIAL PRIMARY KEY,
                filename TEXT UNIQUE NOT NULL,
                url TEXT NOT NULL,
                media_type TEXT DEFAULT NULL
            );
            """
        )

    def insert_media(self, filename, url, media_type=None):
        """ذخیره یک خط در جدول media"""
        self.cursor.execute(
            """
            INSERT INTO media (filename, url, media_type)
            VALUES (%s, %s, %s)
            ON CONFLICT (filename) DO NOTHING
            RETURNING id;
            """,
            (filename, url, media_type),
        )
        row = self.cursor.fetchone()
        return row[0] if row else None

    def get_url_by_filename(self, filename):
        """بازگشت url با اسم فایل"""
        self.cursor.execute(
            "SELECT url FROM media WHERE filename = %s",
            (filename,),
        )
        row = self.cursor.fetchone()
        return row[0] if row else None

    def delete_by_filename(self, filename):
        """حذف فایل با اسم آن"""
        self.cursor.execute("DELETE FROM media WHERE filename = %s", (filename,))
        return self.cursor.rowcount > 0


# 🔹 توابع بیرون کلاس

def create_table():
    with MediaTableManager() as db:
        db.create_table()


def save_media(filename, url, media_type=None):
    with MediaTableManager() as db:
        return db.insert_media(filename, url, media_type)


def get_url(filename):
    with MediaTableManager() as db:
        return db.get_url_by_filename(filename)


def delete_media(filename):
    with MediaTableManager() as db:
        return db.delete_by_filename(filename)
