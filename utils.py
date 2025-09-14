from datetime import datetime
import jdatetime
import io


async def get_media_bytes(message, bot) -> bytes | None:
    file_id = None
    type_file = None
    if message.photo:
        photo = message.photo[-1]
        file_id = photo.id
        type_file = "photo"
    elif message.audio:
        file_id = message.audio.id
        type_file = "audio"
    elif message.video:
        file_id = message.video.id
        type_file = "video"

    if file_id is None:
        return False

    bio = file_id_to_bynery(file_id, bot)
    bin_file = bio.read()
    return bin_file, type_file


async def file_id_to_bynery(file_id, bot):
    content = await bot.download(file_id)
    bio = io.BytesIO(content)
    bio.seek(0)
    return bio


def get_mentioning_the_day():
    daily_data = {
        "Saturday": {
            "fa": "شنبه",
            "zekr": "یا رب العالمین",
            "image_path": "media/mentioning_the_day/day (1).jpg",
            "text": "امروز شنبه است، روزی برای شروع تازه.",
        },
        "Sunday": {
            "fa": "یک‌شنبه",
            "zekr": "یا ذاالجلال و الاکرام",
            "image_path": "media/mentioning_the_day/day (2).jpg",
            "text": "یک‌شنبه، روزی پر از انرژی و امید.",
        },
        "Monday": {
            "fa": "دوشنبه",
            "zekr": "یا قاضی الحاجات",
            "image_path": "media/mentioning_the_day/day (3).jpg",
            "text": "دوشنبه، فرصتی دوباره برای تلاش.",
        },
        "Tuesday": {
            "fa": "سه‌شنبه",
            "zekr": "یا ارحم الراحمین",
            "image_path": "media/mentioning_the_day/day (4).jpg",
            "text": "سه‌شنبه، روز بخشش و مهربانی.",
        },
        "Wednesday": {
            "fa": "چهارشنبه",
            "zekr": "یا حی یا قیوم",
            "image_path": "media/mentioning_the_day/day (5).jpg",
            "text": "چهارشنبه، روزی برای تامل و اندیشه.",
        },
        "Thursday": {
            "fa": "پنج‌شنبه",
            "zekr": "لا اله الا الله الملک الحق المبین",
            "image_path": "media/mentioning_the_day/day (6).jpg",
            "text": "پنج‌شنبه، روز تلاش و موفقیت.",
        },
        "Friday": {
            "fa": "جمعه",
            "zekr": "اللهم صل علی محمد و آل محمد",
            "image_path": "media/mentioning_the_day/day (7).jpg",
            "text": "جمعه، روز آرامش و استراحت.",
        },
    }
    today = datetime.now()
    day_en = today.strftime("%A")
    info = daily_data.get(day_en)

    if not info:
        return "روز نامشخصی است!"

    day_fa = info["fa"]
    zekr = info["zekr"]
    url = info["image_path"]

    today_jalali = jdatetime.datetime.now()
    date_str = today_jalali.strftime("%Y/%m/%d")

    return {
        "name": day_fa,
        "zekr": zekr,
        "date": date_str,
        "path": url,
    }
