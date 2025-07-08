from balethon.objects import InlineKeyboard , InlineKeyboardButton , ReplyKeyboardRemove
from  dotenv import load_dotenv
from balethon import Client
from models import hadith as db_hadith
from models import notes as db_notes
import os 


load_dotenv()


# assignment initial variables...................................

bot = Client(os.getenv('TOKEN'))
group_pajohesh_hadith_id = int(os.getenv('PAJOHESH_HADITH'))
group_pajohesh_notes_id = int(os.getenv('PAJOHESH_NOTES'))
group_mirror_id = int(os.getenv('MIRROR'))
chanel_tamakkon_id = int(os.getenv('CHANNEL_TAMAKKON'))
photo_url =   'photo.jpg'       #os.getenv('POTO_URL')







# create tables ...............................................

db_hadith.create_hadith_table()
db_notes.create_table_note()




# get state for db................................

def get_state():
    hadith_data = db_hadith.get_hadith_data()
    note_data = db_notes.get_note_data()
    total_data = f'📗 آمار احادیث: \n{hadith_data} \n\n\n📕 آمار یادداشت‌ها: \n {note_data}'
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
        [InlineKeyboardButton("گرفتن آمار", "get_stats")],
        [InlineKeyboardButton("بازگشت", "back_to_main")]
        
    )
    
    
def note_menu():
    return InlineKeyboard(
        [InlineKeyboardButton(" ارسال یادداشت", "send_note")],
        [InlineKeyboardButton("ذخیره کردن یادداشت", "save_note")],
        [InlineKeyboardButton("بازگشت", "back_to_message")]
    )

def hadith_menu():
    return InlineKeyboard(
        [InlineKeyboardButton("ارسال تصادفی", "send_random_hadith")],
        [InlineKeyboardButton("ارسال با شماره", "send_hadith_by_number")],
        [InlineKeyboardButton("بازگشت", "back_to_message")]
    )

def answer_y_n(id):
    return InlineKeyboard(
        [InlineKeyboardButton(f"بله", f"resend:{id}")],
        [InlineKeyboardButton("بازگشت", "back_to_message")]
    )

def back_menu():
    return InlineKeyboard(
        [InlineKeyboardButton("بازگشت", "back_to_message")]
    )


