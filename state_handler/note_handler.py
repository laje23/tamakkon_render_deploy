from config import *

MESSAGES = {
    "invalid_number": "❗️ لطفاً فقط عدد مثبت وارد کنید.",
    "note_exists": "این یادداشت موجود است. می‌خواهید آن را ویرایش کنید؟",
    "enter_note_text": "متن یادداشت رو بفرستید",
    "note_saved": "یادداشت با موفقیت ذخیره شد.",
    "note_not_found": "شماره یادداشت پیدا نشد! دوباره امتحان کن.",
    "note_does_not_exist": "این یادداشت موجود نیست. ابتدا آن را ایجاد کنید.",
    "note_sent": "یادداشت ارسال شده است و قابل ویرایش نیست.",
    "note_edited": "یادداشت ویرایش شد.",
    "ask_more_text": "متن بیشتری داری؟ لطفا پاسخ بده: بله / خیر",
    "invalid_answer": "لطفا فقط 'بله' یا 'خیر' جواب بده.",
    "ask_media": "آیا می‌خواهی همراه یادداشت عکس یا فیلمی ارسال کنی؟ اگر داری ارسال کن، اگر نه بنویس 'ندارم'.",
    "media_received": "فایل دریافت شد. حالا لطفاً متن یادداشت رو بفرست.",
    "no_media": "باشه، بدون فایل. حالا لطفاً متن یادداشت رو بفرست.",
    "invalid_media_response": "لطفاً فایل بفرست یا بنویس 'ندارم'.",
}


def fa_to_en_int(num):
    fa_digits = "۰۱۲۳۴۵۶۷۸۹"
    en_digits = "0123456789"
    result = ""
    for ch in str(num):
        if ch in fa_digits:
            result += en_digits[fa_digits.index(ch)]
        elif ch in en_digits:
            result += ch
        else:
            continue
    return int(result)


async def first_step_save(message):
    note_number = fa_to_en_int(message.text)
    if note_number <= 0:
        await bale_bot.send_message(
            message.chat.id, MESSAGES["invalid_number"], back_menu()
        )
        return

    if db_notes.check_is_exist(note_number):
        user_temp_data[message.author.id] = {
            "note_edit_number": note_number,
            "text_parts": [],
        }
        message.author.set_state("INPUT_EDIT_TEXT_NOTE")
        await bale_bot.send_message(
            message.chat.id,
            MESSAGES["note_exists"] + "\n" + MESSAGES["enter_note_text"],
            back_menu(),
        )
    else:
        user_temp_data[message.author.id] = {
            "note_number": note_number,
            "text_parts": [],
        }
        message.author.set_state("ASK_MEDIA")
        await bale_bot.send_message(message.chat.id, MESSAGES["ask_media"])


async def handle_media_step(message):
    user_id = message.author.id
    state = message.author.get_state()

    if state != "ASK_MEDIA":
        return

    if message.photo:
        user_temp_data[user_id]["media_type"] = "photo"
        user_temp_data[user_id]["media_file_id"] = message.photo[-1].id
        await bale_bot.send_message(message.chat.id, MESSAGES["media_received"])
        message.author.set_state("INPUT_TEXT_NOTE")

    elif message.video:
        user_temp_data[user_id]["media_type"] = "video"
        user_temp_data[user_id]["media_file_id"] = message.video.id
        await bale_bot.send_message(message.chat.id, MESSAGES["media_received"])
        message.author.set_state("INPUT_TEXT_NOTE")

    elif message.text and message.text.strip().lower() == "ندارم":
        await bale_bot.send_message(message.chat.id, MESSAGES["no_media"])
        message.author.set_state("INPUT_TEXT_NOTE")

    else:
        await bale_bot.send_message(message.chat.id, MESSAGES["invalid_media_response"])


async def handle_text_parts(message):
    user_id = message.author.id
    state = message.author.get_state()

    if state not in ["INPUT_TEXT_NOTE", "INPUT_EDIT_TEXT_NOTE"]:
        await bale_bot.send_message(
            message.chat.id, MESSAGES["invalid_number"], back_menu()
        )
        return

    text = message.text.strip()

    user_temp_data[user_id]["text_parts"].append(text)
    await bale_bot.send_message(message.chat.id, MESSAGES["ask_more_text"])
    message.author.set_state("CONFIRM_MORE_TEXT")


async def confirm_more_text(message):
    user_id = message.author.id
    answer = message.text.strip().lower()

    if answer == "بله":
        if "note_number" in user_temp_data[user_id]:
            message.author.set_state("INPUT_TEXT_NOTE")
        elif "note_edit_number" in user_temp_data[user_id]:
            message.author.set_state("INPUT_EDIT_TEXT_NOTE")
        await bale_bot.send_message(message.chat.id, MESSAGES["enter_note_text"])

    elif answer == "خیر":
        full_text = "\n".join(user_temp_data[user_id]["text_parts"])

        if "note_number" in user_temp_data[user_id]:
            note_number = user_temp_data[user_id]["note_number"] or ""
            file_id = str(user_temp_data[user_id].get("media_file_id", ""))
            media_type = user_temp_data[user_id].get("media_type", "")
            try:
                db_notes.save_note(note_number, full_text, file_id, media_type)
                await bale_bot.send_message(
                    message.chat.id, MESSAGES["note_saved"], back_menu()
                )
            except Exception as e:
                await bale_bot.send_message(message.chat.id, str(e), back_menu())

        elif "note_edit_number" in user_temp_data[user_id]:
            note_number = user_temp_data[user_id]["note_edit_number"]
            try:
                db_notes.edit_content(note_number, full_text)
                await bale_bot.send_message(
                    message.chat.id, MESSAGES["note_edited"], back_menu()
                )
            except Exception as e:
                await bale_bot.send_message(message.chat.id, str(e), back_menu())

        user_temp_data.pop(user_id, None)
        message.author.del_state()

    else:
        await bale_bot.send_message(message.chat.id, MESSAGES["invalid_answer"])
