from balethon.objects import InlineKeyboard , InlineKeyboardButton 
from balethon import Client
from app_manager import EitaaBot , GapBot
from models import hadith as db_hadith
from models import notes as db_notes
import os 


user_temp_data = {}
# assignment initial variables...................................

bale_bot = Client(os.getenv('BALE_BOT_TOKEN'))
eitaa_bot = EitaaBot(os.getenv('EITAA_BOT_TOKEN'))
gap_bot = GapBot(os.getenv('GAP_BOT_TOKEN'))

debuger_id = 1462760140

group_pajohesh_hadith_id = int(os.getenv('PAJOHESH_HADITH'))

bale_group_mirror_id = int(os.getenv('BALE_MIRROR'))
eitaa_group_mirror_id = int(os.getenv('EITAA_MIRROR'))


bale_channel_id = int(os.getenv('CHANNEL_BALE'))
eitaa_channel_id = int(os.getenv('CHANNEL_EITAA'))

photo_url =   'medai/photo.jpg'       #os.getenv('POTO_URL')
tohid_audio_url = 'media/tohid.mp3'
salavat_audio_url = 'media/salavaat.mp3'




# create tables ...............................................

db_hadith.create_table()
db_notes.create_table()




# get state for db................................

def get_state():
    hadith_data = db_hadith.get_hadith_data()
    note_data = db_notes.get_note_data()
    total_data = f'امار  .... \n{hadith_data} \n\n\n {note_data}'
    return total_data




# process messages  ........................................................
# 🧠 پردازش پیام‌ها
def process_hadith_message(text: str, id: int | str) -> str:
    return f'''{text}

معرفی کتاب:
https://eitaa.com/tamakkon_ir/19


دانلود کتاب:
https://eitaa.com/tamakkon_ir/20

#حدیث
#{id}
@tamakkon_ir'''


def process_note_message(text: str, id: int | str) -> str:
    emoji_map = {i: num for i, num in enumerate(['0️⃣','1️⃣','2️⃣','3️⃣','4️⃣','5️⃣','6️⃣','7️⃣','8️⃣','9️⃣'])}
    emojied = ''.join(emoji_map[int(c)] for c in str(id)[::-1])
    return f'''#یادداشت_استاد
شماره {emojied}

{text}

صفحه رسمی استاد در فارس من:
https://farsnews.ir/shnavvab

#نهضت_تمکن
@tamakkon_ir'''











# keyboard buttens ......................................
# 🧩 کیبوردها



def main_menu(is_admin):
    rows = []
    rows.append([InlineKeyboardButton("در حال بروزرسانی", "in_update")])
    if is_admin:
        rows.append([InlineKeyboardButton("مدیریت پیام ها", "back_to_message")])

    return InlineKeyboard(*rows)

def message_menu():
    return InlineKeyboard(
        [InlineKeyboardButton("حدیث", "hadith_menu")],
        [InlineKeyboardButton("یادداشت", "note_menu")],
        [InlineKeyboardButton("ارسال پیام به کانال ", "send_to_channel")],
        [InlineKeyboardButton("ارسال پیام های جا مانده ", "send_laftovers")],
        [InlineKeyboardButton("گرفتن آمار", "get_stats")],
        [InlineKeyboardButton("بازگشت", "back_to_main")]
        
    )
    
    
def note_menu():
    return InlineKeyboard(
        [InlineKeyboardButton(" ارسال یادداشت", "auto_send_note")],
        [InlineKeyboardButton("یادداشت جدید ", "save_note")],
        [InlineKeyboardButton("ویرایش", "edit_note")],
        [InlineKeyboardButton("بازگشت", "back_to_message")]
    )

def hadith_menu():
    return InlineKeyboard(
        [InlineKeyboardButton("ارسال تصادفی", "auto_send_hadith")],
        [InlineKeyboardButton("بازگشت", "back_to_message")]
    )

def answer_y_n(id):
    return InlineKeyboard(
        [InlineKeyboardButton(f"بله", f"resend:{id}")],
        [InlineKeyboardButton("بازگشت", "back_to_message")]
    )

def edit_menu():
    return InlineKeyboard(
        [InlineKeyboardButton("ویرایش", "edit_note")],
        [InlineKeyboardButton("بازگشت", "back_to_message")]
    )



def back_menu():
    return InlineKeyboard(
        [InlineKeyboardButton("بازگشت", "back_to_message")]
    )
