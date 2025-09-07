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
                sent_bale INTEGER DEFAULT 0,
                sent_eitaa INTEGER DEFAULT 0
            );
        """)

    def update_sent_to_1(self, id):
        self.cursor.execute("UPDATE notes SET sent = 1 WHERE id = %s", (id,))
        

    def insert_content_and_id(self , content , id):
        self.cursor.execute('INSERT INTO notes (id ,content) VALUES(%s,%s)' , (id,content))

    def chak_id_exist(self , id ):
        self.cursor.execute("""
            SELECT (SELECT 1 FROM notes WHERE id = %s);
        """, (id,))
        
        exists = self.cursor.fetchone()[0]
        return exists 
    
    def return_auto_content(self):
        self.cursor.execute(
            'SELECT content , id FROM notes WHERE sent_bale = 0 AND sent_eitaa = 0 ORDER BY id '
        )
        return self.cursor.fetchone()
    
    def select_leftover_bale(self):
        self.cursor.execute(
            'SELECT content,id FROM notes WHERE sent_bale = 0 AND sent_eitaa = 1'
        )
        content = self.cursor.fetchall()
        return content if content else None 
    
    def select_leftover_eitaa(self):
        self.cursor.execute(
            'SELECT content,id FROM notes WHERE sent_bale = 1 AND sent_eitaa = 0'
        )
        content = self.cursor.fetchall()
        return content if content else None 

    def update_sent_bale_to_1(self, id, content):
        self.cursor.execute(
            'UPDATE notes SET sent_bale = %s WHERE id = %s OR content = %s',
            (1, id, content)
        )
    
    def update_sent_eitaa_to_1(self, id, content):
        self.cursor.execute(
            'UPDATE notes SET sent_eitaa = %s WHERE id = %s OR content = %s',
            (1, id, content)
        )

    def update_sent_all_to_1(self, id, content):
        self.cursor.execute(
            'UPDATE hadith SET sent_eitaa = %s , sent_bale = %s WHERE id = %s OR content = %s',
            (1,1, id, content)
        )
        
    def count_sent_status(self):
        self.cursor.execute("""
            SELECT
                SUM(CASE WHEN sent_bale = 1 THEN 1 ELSE 0 END) AS bale_count,
                SUM(CASE WHEN sent_eitaa = 1 THEN 1 ELSE 0 END) AS eitaa_count
            FROM notes
        """)
        result = self.cursor.fetchone()
        return result[0] , result[1]
    
    def return_sents(self , id ):
        self.cursor.execute(
            'SELECT sent_bale , sent_eitaa FROM notes WHERE id = %s',
            (id,)
        )
        result = self.cursor.fetchone()
        return result[0]

    def update_content(self , id , content):
        self.cursor.execute(
            'UPDATE notes SET content = %s WHERE id = %s',
            (content,id)
        )


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
    
def mark_sent_bale(id = 0 , content = ''):
    with NoteTableManager() as db : 
        db.update_sent_bale_to_1(id , content)
    return 

def mark_sent_eitaa(id = 0 , content = ''):
    with NoteTableManager() as db : 
        db.update_sent_eitaa_to_1(id , content)
    return

def mark_sent_all(id = 0 , content = ''):
    with NoteTableManager() as db : 
        db.update_sent_all_to_1(id , content)
    return


def return_bale_laftover():
    with NoteTableManager() as db : 
        return db.select_leftover_bale()


def return_eitaa_laftover():
    with NoteTableManager() as db : 
        return db.select_leftover_eitaa()
    
def count_sent_all():
    with NoteTableManager() as db:
        bale , eitaa  = db.count_sent_status()
        return f'یادداشت ها \n در بله : {bale} \n\n در ایتا : {eitaa}'
    
def return_sent(id):
    with NoteTableManager() as db :
        return db.return_sents(id)
    
    
def edit_content(id , content ):
    with NoteTableManager() as db : 
        db.update_content(id , content)
    return