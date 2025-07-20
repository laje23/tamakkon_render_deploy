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
                content TEXT DEFAULT NULL, 
                sent INTEGER DEFAULT 0
            );
        """)

    def update_sent_to_1(self, id):
        self.cursor.execute("UPDATE notes SET sent = 1 WHERE id = %s", (id,))
        
    def insert_content_and_id(self , content , id):
        self.cursor.execute('INSERT INTO notes (id ,content) VALUES(%s,%s)' , (id,content))

    def chak_id_exist(self , id ):
        self.cursor.execute("""
            SELECT EXISTS(SELECT 1 FROM notes WHERE id = %s);
        """, (id,))
        
        exists = self.cursor.fetchone()[0]
        return exists 
    
    def return_auto_content(self):
        self.cursor.execute(
            'SELECT content , id FROM notes WHERE sent = 0 ORDER BY id '
        )
        return self.cursor.fetchone()



def create_table():
    with NoteTableManager() as db :
        db.create_table()
        
def new_note(id ,content):
    with NoteTableManager() as db :
        db.insert_content_and_id(content,id)

def chek_is_exist(id):
    with NoteTableManager() as db :
        return db.chak_id_exist(id)
    
def auto_return_content() -> tuple:
    with NoteTableManager() as db :
        return db.return_auto_content()
    
def mark_sent(id):
    with NoteTableManager() as db :
        db.update_sent_to_1(id)
    return 