import io

async def get_media_bytes(message, bot) -> bytes | None:
    file_id = None
    type_file = None 
    if message.photo:
        # عکس معمولا لیست هست، بزرگترین عکس آخره
        photo = message.photo[-1]
        file_id = photo.id
        type_file = 'photo'
    elif message.voice:
        file_id = message.voice.file_id
        type_file = 'voice'
    elif message.audio:
        file_id = message.audio.file_id
        type_file = 'audio'
    elif message.video:
        file_id = message.video.file_id
        type_file = 'video'
    elif message.document and hasattr(message.document, 'mime_type'):
        if message.document.mime_type.startswith('audio') or message.document.mime_type.startswith('video') or message.document.mime_type.startswith('image'):
            file_id = getattr(message.document, 'file_id', None) or getattr(message.document, 'id', None)
        type_file = 'document'
    
    if file_id is None:
        return None , None 
    
    content = await bot.download(file_id)
    bio = io.BytesIO(content)
    bio.seek(0)
    return bio.read() , type_file
















from datetime import datetime
import jdatetime

def today():
    days_fa = {
        "Monday": "دوشنبه",
        "Tuesday": "سه‌شنبه",
        "Wednesday": "چهارشنبه",
        "Thursday": "پنج‌شنبه",
        "Friday": "جمعه",
        "Saturday": "شنبه",
        "Sunday": "یک‌شنبه"
    }

    azkar = {
        "شنبه": "یا رب العالمین",
        "یک‌شنبه": "یا ذاالجلال و الاکرام",
        "دوشنبه": "یا قاضی الحاجات",
        "سه‌شنبه": "یا ارحم الراحمین",
        "چهارشنبه": "یا حی یا قیوم",
        "پنج‌شنبه": "لا اله الا الله الملک الحق المبین",
        "جمعه": "اللهم صل علی محمد و آل محمد"
    }

    today = datetime.now()
    day_en = today.strftime("%A")
    day_fa = days_fa.get(day_en, "")

    zekr = azkar.get(day_fa, "")

    # گرفتن تاریخ شمسی
    today_jalali = jdatetime.datetime.now()
    date_str = today_jalali.strftime("%Y/%m/%d")

    return f"امروز {day_fa} - {date_str} \nذکر روز: {zekr}"

