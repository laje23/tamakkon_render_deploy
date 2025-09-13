from balethon.objects import InlineKeyboard, InlineKeyboardButton
from balethon import Client
from app_manager import EitaaBot
from models import hadith as db_hadith
from models import notes as db_notes
from models import clips as db_clips 
from models import books as db_books
import asyncio
import threading
import os

user_temp_data = {}
# assignment initial variables...................................

bale_bot = Client(os.getenv("BALE_BOT_TOKEN"))
eitaa_bot = EitaaBot(os.getenv("EITAA_BOT_TOKEN"))

debugger_id = os.getenv("DEBUGER_ID")

group_reserch_hadith_id = int(os.getenv("RESERCH_HADITH"))
group_reserch_clip_id = int(os.getenv('RESERCH_CLIP_ID'))

bale_channel_id = int(os.getenv("CHANNEL_BALE"))
eitaa_channel_id = int(os.getenv("CHANNEL_EITAA"))


hadith_photo_url = os.getenv("HADITH_POTO_URL")
tohid_audio_url = os.getenv("TOHID_AUDIO_URL")
salavat_audio_url = os.getenv("SALAVAT_AUDIO_URL")
base_day_name_url = os.getenv("BASE_DAY_URL")

admins = [893366360, 1462760140]


# create tables ..............................................
db_hadith.create_table()
db_notes.create_table()
db_clips.create_table()
db_books.create_table()


# process messages  ........................................................
# 🧠 پردازش پیام‌ها
def process_hadith_message(text: str, id: int | str, eitaa=False) -> str:
    if eitaa:
        return f"""{text} \n\nمعرفی کتاب:
    https://eitaa.com/tamakkon_ir/19


    دانلود کتاب:
    https://eitaa.com/tamakkon_ir/20

    #حدیث
    #{id}
    @tamakkon_ir"""

    else:
        return f"""{text}\n\nمعرفی کتاب:
    https://ble.ir/tamakkon_ir/-400893920905783805/1757415117292


    دانلود کتاب:
    https://ble.ir/tamakkon_ir/7588061826126981347/1757415238870

    #حدیث
    #{id}
    @tamakkon_ir"""


def process_note_message(text: str, id: int | str) -> str:
    emoji_map = {
        i: num
        for i, num in enumerate(["0️⃣", "1️⃣", "2️⃣", "3️⃣", "4️⃣", "5️⃣", "6️⃣", "7️⃣", "8️⃣", "9️⃣"])
    }
    emojied = "".join(emoji_map[int(c)] for c in str(id)[::-1])
    return f"""#یادداشت_استاد
شماره {emojied}

{text}

صفحه رسمی استاد در فارس من:
https://farsnews.ir/shnavvab

#نهضت_تمکن
@tamakkon_ir"""


# keyboard buttens ......................................
# 🧩 کیبوردها


def main_menu(is_admin: bool):
    rows = [[InlineKeyboardButton("در حال بروزرسانی", "in_update")]]

    if is_admin:
        rows.append([InlineKeyboardButton("مدیریت پیام‌ها", "back_to_message")])

    return InlineKeyboard(*rows)


def message_menu():
    return InlineKeyboard(
        [InlineKeyboardButton("ارسال ها", "send_menu")],
        [InlineKeyboardButton("یادداشت", "note_menu")],
        [InlineKeyboardButton("ارسال پیام به کانال ", "send_to_channel")],
        [InlineKeyboardButton("ارسال پیام های جا مانده ", "send_laftovers")],
        [InlineKeyboardButton("گرفتن آمار", "get_status")],
        [InlineKeyboardButton("بازگشت", "back_to_main")],
    )


def note_menu():
    return InlineKeyboard(
        [InlineKeyboardButton(" ارسال یادداشت", "auto_send_note")],
        [InlineKeyboardButton("یادداشت جدید ", "save_note")],
        [InlineKeyboardButton("ویرایش", "edit_note")],
        [InlineKeyboardButton("بازگشت", "back_to_message")],
    )


def send_menu():
    return InlineKeyboard(
        [InlineKeyboardButton("ارسال حدیث", "auto_send_hadith")],
        [InlineKeyboardButton("ارسال کتاب", "auto_send_book")],
        [InlineKeyboardButton("ارسال کلیپ", "auto_send_clip")],
        [InlineKeyboardButton("بازگشت", "back_to_message")],
    )


def answer_y_n(id):
    return InlineKeyboard(
        [InlineKeyboardButton(f"بله", f"resend:{id}")],
        [InlineKeyboardButton("بازگشت", "back_to_message")],
    )


def edit_menu():
    return InlineKeyboard(
        [InlineKeyboardButton("ویرایش", "edit_note")],
        [InlineKeyboardButton("بازگشت", "back_to_message")],
    )


def back_menu():
    return InlineKeyboard([InlineKeyboardButton("بازگشت", "back_to_message")])
