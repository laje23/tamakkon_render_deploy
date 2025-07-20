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
                sent INTEGER DEFAULT 0
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

    def update_sent_to_1(self , id ):
        self.cursor.execute(
            'UPDATE hadith SET sent = 1 WHERE id = %s ',
            (id,)
        )

    def update_content(self, message_id, new_content):
        self.cursor.execute(
            'UPDATE hadith SET content = %s WHERE message_id = %s',
            (new_content, message_id)
        )

    def update_sent_to_1(self,id):
        self.cursor.execute(
            'UPDATE hadith SET sent = %s WHERE id = %s',
            (1,id)
        )




def create_table():
    with HadithTabelManager() as db :
        db.create_table()
    return



def save_id_and_content(message_id , content):
    with HadithTabelManager() as db :
        db.insert_row(message_id , content)
    return
        


def message_sent(id):
    with HadithTabelManager() as db :
        db.update_sent_to_1(id)
    return



def edit_content(message_id , new_content):
    with HadithTabelManager() as db :
        db.update_content(message_id , new_content)
    return


def return_auto_content():
    with HadithTabelManager() as db : 
        return db.auto_select_content()


def mark_sent(id):
    with HadithTabelManager() as db : 
        db.update_sent_to_1(id)
    return 