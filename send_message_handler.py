from config import *
from utils import *
import asyncio
from models import clips, books


async def send_to_debugger(err_text):
    if err_text:
        if err_text != " پیام ارسال شد":
            await bale_bot.send_message(debugger_id, err_text)


async def auto_send_hadith():
    result = db_hadith.return_auto_content()
    if not result:
        return "هیچ پیامی موجود نیست"

    content, id = result

    if not os.path.exists(hadith_photo_url):
        return f"عکس موجود نیست: {hadith_photo_url}"

    try:
        with open(hadith_photo_url, "rb") as photo:
            bale = await bale_bot.send_photo(
                bale_channel_id, photo, process_hadith_message(content, id)
            )
            eitaa = await eitaa_bot.send_file(
                eitaa_channel_id, photo, process_hadith_message(content, id, True)
            )

        if not (bale and eitaa):
            raise Exception("حدیث در بله یا ایتا ارسال نشد!")

        db_hadith.mark_sent(id)

    except Exception as e:
        return f" ارور :\n {e}"


async def auto_send_not():
    result = db_notes.auto_return_content()
    if not result:
        return "هیچ پیامی موجود نیست"
    content, id = result
    text = process_note_message(content, id)
    try:
        bale = await bale_bot.send_message(bale_channel_id, text)
        eitaa = await eitaa_bot.send_message(eitaa_channel_id, text)
        if not (bale and eitaa):
            raise Exception("حدیث در بله یا ایتا ارسال نشد!")

        db_notes.mark_sent(id)

    except Exception as e:
        return f" ارور :\n {e}"


async def send_message_to_channel(message, bot):
    if x := await get_media_bytes(message, bot):
        bin_file, typefile = x
        try:
            if typefile == "photo":
                await bale_bot.send_photo(bale_channel_id, bin_file, message.caption)
            elif typefile == "video":
                await bale_bot.send_video(bale_channel_id, bin_file, message.caption)
            # elif typefile == 'voice':
            #     await bale_bot.send_voice(bale_channel_id , bin_file , message.caption )
            elif typefile == "audio":
                await bale_bot.send_audio(bale_channel_id, bin_file, message.caption)

            await eitaa_bot.send_file(eitaa_channel_id, bin_file, message.caption)
            return "پیام ارسال شد"
        except Exception as e:
            return f"خطا در ارسال پیام \n\n{e}"
    else:
        if message.text:
            text = message.text
        elif message.caption:
            text = message.caption
        try:
            await bale_bot.send_message(bale_channel_id, text)
            await eitaa_bot.send_message(eitaa_channel_id, text)
            return "پیام ارسال شد "
        except Exception as e:
            return f"خطا در ارسال پیام \n\n{e}"


async def send_leftover_hadith_bale():
    leftover_hadiths = db_hadith.return_bale_laftover()
    if not leftover_hadiths:
        return "پیامی موجود نیست"

    try:
        with open(hadith_photo_url, "rb") as photo:
            for hadith_text, hadith_id in leftover_hadiths:
                text = process_hadith_message(hadith_text, hadith_id)
                await bale_bot.send_photo(bale_channel_id, photo, text)
                db_hadith.mark_sent_bale(id=hadith_id)
        return "پیام‌ها در بله ارسال شدند"
    except Exception as e:
        return f"خطا در ارسال \n\n{e}"


async def send_leftover_hadith_eitaa():
    leftover_hadiths = db_hadith.return_eitaa_laftover()
    if not leftover_hadiths:
        return "پیامی موجود نیست"

    try:
        with open(hadith_photo_url, "rb") as photo:
            for hadith_text, hadith_id in leftover_hadiths:
                text = process_hadith_message(hadith_text, hadith_id)
                await eitaa_bot.send_file(bale_channel_id, photo, text)
                db_hadith.mark_sent_eitaa(id=hadith_id)
        return "پیام‌ها در ایتا ارسال شدند"
    except Exception as e:
        return f"خطا در ارسال \n\n{e}"


async def send_laftover_hadith():
    bale = await send_leftover_hadith_bale()
    eitaa = await send_leftover_hadith_eitaa()
    return f"ایتا \n {eitaa} \n\n بله \n {bale}"


async def send_leftover_note_eitaa():
    leftover_hadiths = db_notes.return_eitaa_laftover()
    if not leftover_hadiths:
        return "پیامی موجود نیست"

    try:
        for hadith_text, hadith_id in leftover_hadiths:
            text = process_note_message(hadith_text, hadith_id)
            await eitaa_bot.send_message(bale_channel_id, text)
            db_notes.mark_sent_eitaa(id=hadith_id)
        return "پیام‌ها در ایتا ارسال شدند"
    except Exception as e:
        return f"خطا در ارسال \n\n{e}"


async def send_leftover_note_bale():
    leftover_hadiths = db_notes.return_bale_laftover()
    if not leftover_hadiths:
        return "پیامی موجود نیست"

    try:
        for hadith_text, hadith_id in leftover_hadiths:
            text = process_note_message(hadith_text, hadith_id)
            await bale_bot.send_message(bale_channel_id, text)
            db_notes.mark_sent_bale(id=hadith_id)
        return "پیام‌ها در بله ارسال شدند"
    except Exception as e:
        return f"خطا در ارسال \n\n{e}"


async def send_laftover_note():
    bale = await send_leftover_note_bale()
    eitaa = await send_leftover_note_eitaa()
    return f"ایتا \n {eitaa} \n\n بله \n {bale}"


async def send_text_schaduler(text):
    try:
        bale = bale_bot.send_message(bale_channel_id, text)
        eitaa = eitaa_bot.send_message(eitaa_channel_id, text)
        await asyncio.gather(bale, eitaa)
    except Exception as e:
        return str(e)


async def send_tohid(time):

    reminders = {
        "06:00": """صبح‌تون نورانی به ذکر خدا
    روز رو با تلاوت سوره مبارکه توحید شروع کنیم.
    بیاید همین حالا با صوتی که گذاشتیم، همگی با هم بخونیم:
    «قُلْ هُوَ اللّهُ أَحَد» 🌸
    انرژی روزتون رو از یاد خدا بگیرید 🙏

    #یادآور_بندگی
    @tamakkon_ir""",
        "12:00": """در میانه روز، وقتیه که دل‌هامون به یک آرامش دوباره نیاز داره.
    بیاید چند لحظه‌ای همه با هم سوره مبارکه توحید رو تلاوت کنیم.
    این ذکر نورانی، بهترین استراحت برای قلب و روح ماست 💫

    #یادآور_بندگی
    @tamakkon_ir""",
        "16:00": """غروب که می‌شه، بهترین زمان برای تازه کردن عهد با خداست.
    بیاید همین حالا همراه صوت سوره مبارکه توحید، همه با هم بخونیم و دل‌هامون رو روشن‌تر کنیم 🌅
    «اللّهُ الصَّمَد»؛ او بی‌نیاز است و ما همه محتاج او 🙏

    #یادآور_بندگی
    @tamakkon_ir""",
        "22:00": """پایان روز، بهترین موقع برای آرامش گرفتن از یاد خداست.
    بیاید پیش از خواب، سوره مبارکه توحید رو با هم بخونیم.
    این نور قرائت، بهترین همراه برای شب‌هامون خواهد بود 🌙💤

    #یادآور_بندگی
    @tamakkon_ir""",
    }

    text = reminders[time]

    try:
        with open(tohid_audio_url, "rb") as v:
            await bale_bot.send_audio(bale_channel_id, v, caption=f"{text}")
            await eitaa_bot.send_file(eitaa_channel_id, v, caption=f"{text}")

    except Exception as e:
        return str(e)


async def send_salavat_8():
    text = """✨ بیاید با صلوات خاص امام رضا (ع) دل‌هامون رو روشن کنیم 🌟
اللهم صلّ علی علی بن موسی الرضا 🌹

#یادآور_خادمی
@tamakkon_ir"""

    try:
        with open(salavat_audio_url, "rb") as v:
            await eitaa_bot.send_file(eitaa_channel_id, v, caption=f"{text}")
            await bale_bot.send_audio(bale_channel_id, v, caption=f"{text}")

    except Exception as e:
        return str(e)


async def send_day_info():
    day = get_mentioning_the_day()
    text = f"""یک صبح دیگر شروع شد بیاید با خواندن ذکر امروز و اهدای ثواب آن برای تعجیل حضرت حجت (عج)
در ظهور آن حضرت سهیم باشم
امروز {day['name']} تاریخ {day['date']} 
ذکر روز {day['zekr']}"""

    try:
        bale = await bale_bot.send_photo(bale_channel_id, day["path"], text)
        eitaa = await eitaa_bot.send_file(eitaa_channel_id, day["path"], text)

        if not (bale and eitaa):
            raise Exception("پیام در بله یا ایتا ارسال نشد!")

    except Exception as e:
        return e


async def send_auto_clip():
    id, file_id, text = clips.auto_return_file_id()
    bin_fil = await file_id_to_bynery(file_id, bale_bot)

    try:
        bale = await bale_bot.send_video(
            bale_channel_id, bin_fil.read(), caption=(text or "")
        )
        eitaa = await eitaa_bot.send_file(
            eitaa_channel_id, bin_fil, caption=(text or "")
        )

        if not (bale and eitaa):
            raise Exception("پیام در بله یا ایتا ارسال نشد!")

        clips.mark_clip_sent(id)
    except Exception as e:
        return e


async def send_auto_book():
    book = books.get_unsent_book()
    text = f"""
📖 کتاب امروز

«{book['title']}» نوشته‌ی {book['author']}، منتشر شده توسط {book['publisher'] or 'ناشر نامشخص'}.

🕊️ بخشی از کتاب:
«{book['excerpt'] or '...' }»

این کتاب نگاهی آرام و اندیشمندانه به مفاهیم معنوی و ظهور حضرت مهدی (عج) است. اگر اهل تأمل هستید، شاید این چند صفحه برایتان الهام‌بخش باشد.

#کتاب #مطالعه #{book['id']}
"""
    try:
        bale = await bale_bot.send_message(bale_channel_id, text)
        eitaa = await eitaa_bot.send_message(eitaa_channel_id, text)

        if not (bale and eitaa):
            raise Exception("پیام در بله یا ایتا ارسال نشد!")

        books.mark_book_sent(book["id"])
    except Exception as e:
        return e
