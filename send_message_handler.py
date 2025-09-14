from config import *
from utils import (
    success_response,
    error_response,
    get_media_bytes,
    file_id_to_bynery,
    get_mentioning_day,
)


# 📌 لاگ‌گیری فقط در صورت شکست
async def send_to_debugger(result, chat_id=None):
    if isinstance(result, dict) and not result.get("success", True):
        message = result.get("message", "خطای نامشخص")
        target = chat_id or debugger_id
        try:
            await bale_bot.send_message(target, message)
        except Exception as e:
            print(f"[Debugger Error] ارسال پیام به دیباگر شکست خورد:\n{e}")


# 📤 ارسال حدیث خودکار
async def auto_send_hadith():
    result = db_hadith.return_auto_content()
    if not result:
        return error_response("هیچ پیامی موجود نیست")

    content, id = result

    if not os.path.exists(hadith_photo_url):
        return error_response(f"عکس موجود نیست: {hadith_photo_url}")

    try:
        with open(hadith_photo_url, "rb") as photo:
            await bale_bot.send_photo(
                bale_channel_id, photo, process_hadith_message(content, id)
            )
            await eitaa_bot.send_file(
                eitaa_channel_id, photo, process_hadith_message(content, id, True)
            )

        db_hadith.mark_sent(id)
        return success_response("حدیث ارسال شد")
    except Exception as e:
        return error_response(f"ارور در ارسال حدیث:\n{e}")


# 📤 ارسال یادداشت خودکار
async def auto_send_not():
    result = db_notes.auto_return_content()
    if not result:
        return error_response("هیچ پیامی موجود نیست")

    content, id = result
    text = process_note_message(content, id)

    try:
        await bale_bot.send_message(bale_channel_id, text)
        await eitaa_bot.send_message(eitaa_channel_id, text)

        db_notes.mark_sent(id)
        return success_response("یادداشت ارسال شد")
    except Exception as e:
        return error_response(f"ارور در ارسال یادداشت:\n{e}")


# 📤 ارسال پیام به کانال
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
            return error_response(f"خطا در ارسال پیام:\n{e}")
    else:
        text = message.text or message.caption
        try:
            await bale_bot.send_message(bale_channel_id, text)
            await eitaa_bot.send_message(eitaa_channel_id, text)
            return success_response("پیام ارسال شد")
        except Exception as e:
            return error_response(f"خطا در ارسال پیام متنی:\n{e}")


# 📤 ارسال باقی‌مانده‌های حدیث
async def send_leftover_hadith_bale():
    leftover = db_hadith.return_bale_laftover()
    if not leftover:
        return error_response("پیامی موجود نیست")

    try:
        with open(hadith_photo_url, "rb") as photo:
            for text, id in leftover:
                msg = process_hadith_message(text, id)
                await bale_bot.send_photo(bale_channel_id, photo, msg)
                db_hadith.mark_sent_bale(id=id)
        return success_response("پیام‌ها در بله ارسال شدند")
    except Exception as e:
        return error_response(f"خطا در ارسال بله:\n{e}")


async def send_leftover_hadith_eitaa():
    leftover = db_hadith.return_eitaa_laftover()
    if not leftover:
        return error_response("پیامی موجود نیست")

    try:
        with open(hadith_photo_url, "rb") as photo:
            for text, id in leftover:
                msg = process_hadith_message(text, id)
                await eitaa_bot.send_file(eitaa_channel_id, photo, msg)
                db_hadith.mark_sent_eitaa(id=id)
        return success_response("پیام‌ها در ایتا ارسال شدند")
    except Exception as e:
        return error_response(f"خطا در ارسال ایتا:\n{e}")


async def send_laftover_hadith():
    bale = await send_leftover_hadith_bale()
    eitaa = await send_leftover_hadith_eitaa()
    return success_response(
        "گزارش ارسال", data={"بله": bale["message"], "ایتا": eitaa["message"]}
    )


# 📤 ارسال باقی‌مانده‌های یادداشت
async def send_leftover_note_bale():
    leftover = db_notes.return_bale_laftover()
    if not leftover:
        return error_response("پیامی موجود نیست")

    try:
        for text, id in leftover:
            msg = process_note_message(text, id)
            await bale_bot.send_message(bale_channel_id, msg)
            db_notes.mark_sent_bale(id=id)
        return success_response("یادداشت‌ها در بله ارسال شدند")
    except Exception as e:
        return error_response(f"خطا در ارسال یادداشت‌ها به بله:\n{e}")


async def send_leftover_note_eitaa():
    leftover = db_notes.return_eitaa_laftover()
    if not leftover:
        return error_response("پیامی موجود نیست")

    try:
        for text, id in leftover:
            msg = process_note_message(text, id)
            await eitaa_bot.send_message(eitaa_channel_id, msg)
            db_notes.mark_sent_eitaa(id=id)
        return success_response("یادداشت‌ها در ایتا ارسال شدند")
    except Exception as e:
        return error_response(f"خطا در ارسال یادداشت‌ها به ایتا:\n{e}")


async def send_laftover_note():
    bale = await send_leftover_note_bale()
    eitaa = await send_leftover_note_eitaa()
    return success_response(
        "گزارش ارسال", data={"بله": bale["message"], "ایتا": eitaa["message"]}
    )


# ⏰ پیام زمان‌بندی‌شده
async def send_text_schaduler(text):
    try:
        await asyncio.gather(
            bale_bot.send_message(bale_channel_id, text),
            eitaa_bot.send_message(eitaa_channel_id, text),
        )
        return success_response("پیام زمان‌بندی‌شده ارسال شد")
    except Exception as e:
        return error_response(f"خطا در ارسال پیام زمان‌بندی‌شده:\n{e}")


# 📿 ارسال پیام توحید
async def send_tohid(time):
    text = tohid_reminders.get(time)
    if not text:
        return error_response("زمان نامعتبر است")

    try:
        with open(tohid_audio_url, "rb") as v:
            await asyncio.gather(
                bale_bot.send_audio(bale_channel_id, v, caption=text),
                eitaa_bot.send_file(eitaa_channel_id, v, caption=text),
            )
        return success_response("پیام توحید ارسال شد")
    except Exception as e:
        return error_response(f"خطا در ارسال پیام توحید:\n{e}")


# 🌹 ارسال صلوات خاص
async def send_salavat_8():
    text = """✨ بیاید با صلوات خاص امام رضا (ع) دل‌هامون رو روشن کنیم 🌟
اللهم صلّ علی علی بن موسی الرضا 🌹

#یادآور_خادمی
@tamakkon_ir"""

    try:
        with open(salavat_audio_url, "rb") as v:
            await asyncio.gather(
                eitaa_bot.send_file(eitaa_channel_id, v, caption=text),
                bale_bot.send_audio(bale_channel_id, v, caption=text),
            )
        return success_response("صلوات ارسال شد")
    except Exception as e:
        return error_response(f"خطا در ارسال صلوات:\n{e}")


# 📆 ارسال ذکر روز
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
        return error_response(f"خطا در ارسال ذکر روز:\n{e}")


# 📤 ارسال کلیپ خودکار
async def send_auto_clip():
    try:
        id, file_id, text = db_clips.auto_return_file_id()
        bin_fil = await file_id_to_bynery(file_id, bale_bot)

        await asyncio.gather(
            bale_bot.send_video(bale_channel_id, bin_fil.read(), caption=(text or "")),
            eitaa_bot.send_file(eitaa_channel_id, bin_fil, caption=(text or "")),
        )

        db_clips.mark_clip_sent(id)
        return success_response("کلیپ ارسال شد")
    except Exception as e:
        return error_response(f"خطا در ارسال کلیپ:\n{e}")


# 📚 ارسال کتاب خودکار
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

این کتاب نگاهی آرام و اندیشمندانه به مفاهیم معنوی و ظهور حضرت مهدی (عج) است. اگر اهل تأمل هستید، شاید این چند صفحه برایتان الهام‌بخش باشد.

#کتاب #مطالعه #{book['id']}
"""

        await asyncio.gather(
            bale_bot.send_message(bale_channel_id, text),
            eitaa_bot.send_message(eitaa_channel_id, text),
        )

        db_books.mark_book_sent(book["id"])
        return success_response("کتاب ارسال شد")
    except Exception as e:
        return error_response(f"خطا در ارسال کتاب:\n{e}")
