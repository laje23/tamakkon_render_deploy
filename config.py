from balethon.objects import InlineKeyboard, InlineKeyboardButton
from balethon import Client
from app_manager import EitaaBot
from models import hadith as db_hadith
from models import notes as db_notes
from models import clips as db_clips
from models import books as db_books
from models import lecture as db_lecture
import asyncio
import threading
import os


user_temp_data = {}
# assignment initial variables...................................

bale_bot = Client(os.getenv("BALE_BOT_TOKEN"), time_out=60.0)
eitaa_bot = EitaaBot(os.getenv("EITAA_BOT_TOKEN"))

debugger_id = os.getenv("DEBUGER_ID")

group_reserch_hadith_id = int(os.getenv("RESERCH_HADITH"))
group_reserch_clip_id = int(os.getenv("RESERCH_CLIP_ID"))
group_reserch_lecture_id = int(os.getenv("RESERCH_LECTURE_ID"))


bale_channel_id = int(os.getenv("CHANNEL_BALE"))
eitaa_channel_id = int(os.getenv("CHANNEL_EITAA"))


base_image_url = os.getenv("BASE_IMAGE_URL")
base_mentioning_image_url = os.getenv("BASE_DAY_URL")
base_audio_url = os.getenv("BASE_AUDIO_URL")


hadith_photo_url = base_image_url + "hadith.jpg"


tohid_audio_url = base_audio_url + "Tohid.mp3"
prayer_salavaat_url = base_audio_url + "Salavaat.mp3"
Prayer_faraj_url = base_audio_url + "Faraj.mp3"
Prayer_ahd_url = base_audio_url + "Ahd.mp3"


admins = [
    int(admin_id)
    for admin_id in os.getenv("ADMINS_ID", "").split(",")
    if admin_id.strip()
]

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
        [InlineKeyboardButton("کتاب ها", "book_menu")],
        [InlineKeyboardButton("ارسال پیام به کانال ", "send_to_channel")],
        [InlineKeyboardButton("گرفتن آمار", "get_status")],
        [InlineKeyboardButton("بازگشت", "back_to_main")],
    )


def note_menu():
    return InlineKeyboard(
        [InlineKeyboardButton("یادداشت جدید ", "save_note")],
        [InlineKeyboardButton("ویرایش", "edit_note")],
        [InlineKeyboardButton("بازگشت", "back_to_message")],
    )


def book_menu():
    return InlineKeyboard(
        [InlineKeyboardButton("کتاب جدید ", "save_book")],
        [InlineKeyboardButton("ویرایش", "edit_book")],
        [InlineKeyboardButton("بازگشت", "back_to_message")],
    )


def save_or_edit_menu():
    return InlineKeyboard(
        [InlineKeyboardButton("یادداشت", "note_menu")],
        [InlineKeyboardButton("کتاب", "book_menu")],
        [InlineKeyboardButton("بازگشت", "back_to_message")],
    )


def send_menu():
    return InlineKeyboard(
        [InlineKeyboardButton("حدیث", "auto_send_hadith")],
        [InlineKeyboardButton("یادداشت", "auto_send_note")],
        [InlineKeyboardButton("کتاب", "auto_send_book")],
        [InlineKeyboardButton("کلیپ", "auto_send_clip")],
        [InlineKeyboardButton("بازگشت", "back_to_message")],
    )


def answer_y_n(id):
    return InlineKeyboard(
        [InlineKeyboardButton(f"بله", f"resend:{id}")],
        [InlineKeyboardButton("بازگشت", "back_to_message")],
    )


def edit_note_menu():
    return InlineKeyboard(
        [InlineKeyboardButton("ویرایش", "edit_note")],
        [InlineKeyboardButton("بازگشت", "back_to_message")],
    )


def back_menu():
    return InlineKeyboard([InlineKeyboardButton("بازگشت", "back_to_message")])


tohid_reminders = {
    "06:00": """صبح‌تون نورانی به ذکر خدا 🌅
روز رو با تلاوت سوره مبارکه توحید شروع کنیم.
«قُلْ هُوَ اللّهُ أَحَد» 🌸

#یادآور_بندگی
@tamakkon_ir""",
    "12:00": """در میانه روز، وقتیه که دل‌هامون به یک آرامش دوباره نیاز داره 💫
بیاید چند لحظه‌ای سوره مبارکه توحید رو تلاوت کنیم.

#یادآور_بندگی
@tamakkon_ir""",
    "16:00": """غروب که می‌شه، بهترین زمان برای تازه کردن عهد با خداست 🌇
«اللّهُ الصَّمَد»؛ او بی‌نیاز است و ما همه محتاج او 🙏

#یادآور_بندگی
@tamakkon_ir""",
    "22:00": """پایان روز، بهترین موقع برای آرامش گرفتن از یاد خداست 🌙
بیاید پیش از خواب، سوره مبارکه توحید رو با هم بخونیم.

#یادآور_بندگی
@tamakkon_ir""",
}


prayers = {
    "faraj": {
        "url": Prayer_faraj_url,
        "caption": """🌸 دعای فرج

با دعای فرج، دل‌ها آرام و جان‌ها سرشار از امید می‌شود.
فراموش نکنیم امروز نیز با این دعا، ظهور مولایمان حضرت ولی‌عصر (عج) را طلب کنیم. 🌹

#یادآور_فرج
@tamakkon_ir""",
        "local": True,
    },
    "ahd": {
        "url": Prayer_ahd_url,
        "caption": """🌅 دعای عهد

با دعای عهد، پیمان قلبی‌مان با امام زمان (عج) را تازه می‌کنیم.
هر صبح با این دعا، امید و عهدی نو در دل‌ها زنده می‌شود. 💫

#دعای_عهد
@tamakkon_ir""",
        "local": True,
    },
    "salavat": {
        "url": prayer_salavaat_url,
        "caption": """✨ بیاید با صلوات خاص امام رضا (ع) دل‌هامون رو روشن کنیم 🌟
اللهم صلّ علی علی بن موسی الرضا 🌹

#یادآور_خادمی
@tamakkon_ir""",
        "local": True,
    },
}
