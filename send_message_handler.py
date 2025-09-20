from config import *
from typing import Literal
import json
from utils import (
    success_response,
    error_response,
    get_media_bytes,
    file_id_to_bynery,
    get_mentioning_day,
    split_text_with_index,
)


async def send_to_debugger(result, success=False):
    target = debugger_id
    message = (
        result.get("message", "پیام نامشخص")
        if isinstance(result, dict)
        else str(result)
    )
    if success or (isinstance(result, dict) and not result.get("success", True)):
        try:
            await bale_bot.send_message(target, message)
        except Exception as e:
            pass


async def auto_send_hadith():
    result = db_hadith.return_auto_content()
    if not result:
        return error_response("هیچ پیامی موجود نیست")

    content, id = result

    try:
        await bale_bot.send_message(
            bale_channel_id, process_hadith_message(content, id)
        )
        await eitaa_bot.send_message(
            eitaa_channel_id, process_hadith_message(content, id)
        )
        db_hadith.mark_sent(id)
        return success_response("حدیث ارسال شد")
    except Exception as e:
        return error_response("ارور در ارسال حدیث", e)


async def auto_send_not():
    result = db_notes.auto_return_content()
    if not result:
        return error_response("هیچ پیامی موجود نیست")

    content, id, file_id, media_type = result
    chunk_size = 3500
    messages = split_text_with_index(content, chunk_size)

    try:
        if file_id:
            file = await file_id_to_bynery(file_id, bale_bot)
            if media_type == "photo":
                await bale_bot.send_photo(
                    bale_channel_id, file.read(), process_note_message(messages[0], id)
                )
            if media_type == "video":
                await bale_bot.send_video(
                    bale_channel_id, file.read(), process_note_message(messages[0], id)
                )
            await eitaa_bot.send_file(
                eitaa_channel_id, file, process_note_message(messages[0], id)
            )
            messages.pop(0)

        for text in messages:
            await bale_bot.send_message(bale_channel_id, process_note_message(text, id))
            await eitaa_bot.send_message(
                eitaa_channel_id, process_note_message(text, id)
            )

        db_notes.mark_sent(id)
        return success_response("یادداشت ارسال شد")
    except Exception as e:
        return error_response("ارور در ارسال یادداشت", e)


async def send_message_to_channel(message, bot):
    if x := await get_media_bytes(message, bot):
        bin_file, typefile = x
        try:
            if typefile == "photo":
                await bale_bot.send_photo(bale_channel_id, bin_file, message.caption)
            elif typefile == "video":
                await bale_bot.send_video(bale_channel_id, bin_file, message.caption)
            elif typefile == "audio":
                await bale_bot.send_audio(bale_channel_id, bin_file, message.caption)
            await eitaa_bot.send_file(eitaa_channel_id, bin_file, message.caption)
            return success_response("پیام ارسال شد")
        except Exception as e:
            return error_response("خطا در ارسال پیام", e)
    else:
        text = message.text or message.caption
        try:
            await bale_bot.send_message(bale_channel_id, text)
            await eitaa_bot.send_message(eitaa_channel_id, text)
            return success_response("پیام ارسال شد")
        except Exception as e:
            return error_response("خطا در ارسال پیام متنی", e)


async def send_day_info():
    day = get_mentioning_day()
    text = f"""یک صبح دیگر شروع شد بیاید با خواندن ذکر امروز و اهدای ثواب آن برای تعجیل حضرت حجت (عج)
در ظهور آن حضرت سهیم باشم
امروز {day['name']} تاریخ {day['date']} 
ذکر روز {day['zekr']}"""

    try:
        await asyncio.gather(
            bale_bot.send_photo(bale_channel_id, day["path"], text),
            eitaa_bot.send_file(eitaa_channel_id, day["path"], text),
        )
        return success_response("ذکر روز ارسال شد")
    except Exception as e:
        return error_response("خطا در ارسال ذکر روز", e)


async def send_auto_clip():
    try:
        id, file_id, text = db_clips.auto_return_file_id()
        bin_fil = await file_id_to_bynery(file_id, bale_bot)
        text = (text or "") + "\n\n" + "#کلیپ\n@tamakkon_ir"

        await asyncio.gather(
            bale_bot.send_video(bale_channel_id, bin_fil.read(), caption=text),
            eitaa_bot.send_file(eitaa_channel_id, bin_fil, caption=text),
        )
        db_clips.mark_clip_sent(id)
        return success_response("کلیپ ارسال شد")
    except Exception as e:
        return error_response("خطا در ارسال کلیپ", e)


async def send_auto_book():
    try:
        book = db_books.get_unsent_book()
        if not book:
            return error_response("کتاب جدیدی برای ارسال وجود ندارد")

        text = f"""
📖 کتاب امروز

«{book['title']}» نوشته‌ی {book['author']}، منتشر شده توسط {book['publisher'] or 'ناشر نامشخص'}.

🕊️ بخشی از کتاب:
«{book['excerpt'] or '...' }»

معرفی این کتاب، تلاشی است در مسیر شناخت بیشتر نسبت به حضرت ولی‌عصر (عج) و نهضت تمکّن.
امید آن‌که با مطالعه و انس با این آثار، گامی در جهت تعمیق معرفت، تقویت ایمان و آمادگی برای ظهور برداشته شود.

🌹 اللهم عجل لولیک الفرج 🌹

#معرفی_کتاب
@tamakkon_ir
"""

        await asyncio.gather(
            bale_bot.send_message(bale_channel_id, text),
            eitaa_bot.send_message(eitaa_channel_id, text),
        )
        db_books.mark_book_sent(book["id"])
        return success_response("کتاب ارسال شد")
    except Exception as e:
        return error_response("خطا در ارسال کتاب", e)


import asyncio


async def send_prayer(prayer_type: Literal["faraj", "ahd", "salavat", "tohid"]):
    try:
        prayer = prayers.get(prayer_type)
        if not prayer:
            result = error_response(
                "نوع دعای وارد شده معتبر نیست. از 'faraj'، 'ahd' یا 'salavat'  یا 'tohid 'استفاده کنید."
            )
            await send_to_debugger(result)
            return result

        if prayer["local"]:
            if not os.path.exists(prayer["url"]):
                result = error_response(f"فایل صوتی وجود ندارد: {prayer['url']}")
                await send_to_debugger(result)
                return result

            with open(prayer["url"], "rb") as audio_file:
                audio_data = audio_file.read()

            await asyncio.gather(
                bale_bot.send_audio(
                    bale_channel_id, audio_data, caption=prayer["caption"]
                ),
                eitaa_bot.send_file(
                    eitaa_channel_id, audio_data, caption=prayer["caption"]
                ),
            )
        else:
            await asyncio.gather(
                bale_bot.send_audio(
                    bale_channel_id, prayer["url"], caption=prayer["caption"]
                ),
                eitaa_bot.send_file(
                    eitaa_channel_id, prayer["url"], caption=prayer["caption"]
                ),
            )

        result = success_response(f"دعای {prayer_type} ارسال شد")
        await send_to_debugger(result, success=True)
        return result

    except Exception as e:
        result = error_response(f"خطا در ارسال دعای {prayer_type}", e)
        await send_to_debugger(result)
        return result


async def send_auto_lecture():
    try:
        result = db_lecture.auto_return_lecture()
        if not result:
            return error_response("هیچ سخنرانی آماده ارسال نیست")

        id, file_id, caption = result
        bin_file = await file_id_to_bynery(file_id, bale_bot)
        caption = (caption or "") + "\n\n#سخنرانی\n@tamakkon_ir"

        await asyncio.gather(
            bale_bot.send_audio(bale_channel_id, bin_file.read(), caption=caption),
            eitaa_bot.send_file(eitaa_channel_id, bin_file, caption=caption),
        )
        db_lecture.mark_lecture_sent(id)
        return success_response("سخنرانی ارسال شد")
    except Exception as e:
        return error_response("خطا در ارسال سخنرانی", e)
