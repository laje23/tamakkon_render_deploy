from models.database_connection import get_connection

class HadithTabelManager:
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
            CREATE TABLE IF NOT EXISTS hadith (
                id SERIAL PRIMARY KEY,
                message_id INTEGER DEFAULT NULL,
                content TEXT DEFAULT NULL,
                sent_bale INTEGER DEFAULT 0,
                sent_eitaa INTEGER DEFAULT 0
            );
        """)

    def insert_row(self , message_id , content ):
        self.cursor.execute(
            'INSERT INTO hadith (message_id , content) VALUES (%s,%s) ',
            (message_id , content)
            
        )

    def auto_select_content(self):
        self.cursor.execute(
            'SELECT content , id FROM hadith WHERE sent = 0 ORDER BY id LIMIT 1'
        )
        content = self.cursor.fetchone()
        return content if content else None 

    def update_content(self, message_id, new_content):
        self.cursor.execute(
            'UPDATE hadith SET content = %s WHERE message_id = %s',
            (new_content, message_id)
        )

    def update_sent_bale_to_1(self, id, content):
        self.cursor.execute(
            'UPDATE hadith SET sent_bale = %s WHERE id = %s OR content = %s',
            (1, id, content)
        )
    
    def update_sent_eitaa_to_1(self, id, content):
        self.cursor.execute(
            'UPDATE hadith SET sent_eitaa = %s WHERE id = %s OR content = %s',
            (1, id, content)
        )
    
    def select_leftover_bale(self):
        self.cursor.execute(
            'SELECT content,id FROM hadith WHERE sent_bale = 0 AND sent_eitaa = 1'
        )
        content = self.cursor.fetchall()
        return content if content else None 
    
    def select_leftover_eitaa(self):
        self.cursor.execute(
            'SELECT content,id FROM hadith WHERE sent_bale = 1 AND sent_eitaa = 0'
        )
        content = self.cursor.fetchall()
        return content if content else None 

    def update_sent_all_to_1(self, id, content):
        self.cursor.execute(
            'UPDATE hadith SET sent_eitaa = %s , sent_bale = %s WHERE id = %s OR content = %s',
            (1,1, id, content)
        )



def create_table():
    with HadithTabelManager() as db :
        db.create_table()
    return



def save_id_and_content(message_id , content):
    with HadithTabelManager() as db :
        db.insert_row(message_id , content)
    return
        



def edit_content(message_id , new_content):
    with HadithTabelManager() as db :
        db.update_content(message_id , new_content)
    return


def return_auto_content():
    with HadithTabelManager() as db : 
        return db.auto_select_content()


def mark_sent_bale(id = 0 , content = ''):
    with HadithTabelManager() as db : 
        db.update_sent_bale_to_1(id , content)
    return 

def mark_sent_eitaa(id = 0 , content = ''):
    with HadithTabelManager() as db : 
        db.update_sent_eitaa_to_1(id , content)
    return

def mark_sent_all(id = 0 , content = ''):
    with HadithTabelManager() as db : 
        db.update_sent_all_to_1(id , content)
    return


def return_bale_laftover():
    with HadithTabelManager() as db : 
        return db.select_leftover_bale()

def return_eitaa_laftover():
    with HadithTabelManager() as db : 
        return db.select_leftover_eitaa()
    

    
