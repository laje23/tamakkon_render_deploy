from config import *


def fa_to_en_int(num):
    fa_digits = '۰۱۲۳۴۵۶۷۸۹'
    en_digits = '0123456789'
    result = ''
    for ch in str(num):
        if ch in fa_digits:
            result += en_digits[fa_digits.index(ch)]
        elif ch in en_digits:
            result += ch
        else:
            continue  # یا raise ValueError برای کاراکترهای نامعتبر
    return int(result)



# پیام‌های ثابت
MSG_INVALID_NUMBER = "❗️ لطفاً فقط عدد مثبت وارد کنید."
MSG_NOTE_EXISTS = "این یادداشت موجود است. می‌خواهید آن را ویرایش کنید؟"
MSG_ENTER_NOTE_TEXT = "متن یادداشت رو بفرستید"
MSG_NOTE_SAVED = "یادداشت با موفقیت ذخیره شد."
MSG_NOTE_NOT_FOUND = "شماره یادداشت پیدا نشد! دوباره امتحان کن."
MSG_NOTE_DOES_NOT_EXIST = "این یادداشت موجود نیست. ابتدا آن را ایجاد کنید."
MSG_NOTE_SENT = "یادداشت ارسال شده است و قابل ویرایش نیست."
MSG_NOTE_EDITED = "یادداشت ویرایش شد."


async def first_step_save(message):
    note_number = fa_to_en_int(message.text)
    
    if note_number <= 0:
        await bale_bot.send_message(message.chat.id, MSG_INVALID_NUMBER, back_menu())
        return

    if db_notes.check_is_exist(int(note_number)):
        # به جای حذف state، مستقیم وارد حالت ویرایش شو
        user_temp_data[message.author.id] = {"note_edit_number": note_number}
        message.author.set_state("INPUT_EDIT_TEXT_NOTE")
        await bale_bot.send_message(message.chat.id, MSG_NOTE_EXISTS + "\n" + MSG_ENTER_NOTE_TEXT, back_menu())
        return

    user_temp_data[message.author.id] = {"note_number": note_number}
    message.author.set_state("INPUT_TEXT_NOTE")
    await bale_bot.send_message(message.chat.id, MSG_ENTER_NOTE_TEXT)



async def next_step_save(message):
    user_id = message.author.id
    note_number = user_temp_data.get(user_id, {}).get("note_number")

    if not note_number:
        await bale_bot.send_message(message.chat.id, MSG_NOTE_NOT_FOUND, back_menu())
        message.author.del_state()
        return

    try:
        db_notes.save_note(note_number, message.text)
        await bale_bot.send_message(message.chat.id, MSG_NOTE_SAVED, back_menu())
    except Exception as e:
        await bale_bot.send_message(message.chat.id, str(e), back_menu())

    user_temp_data.pop(user_id, None)


async def first_state_edit(message):
    note_number = fa_to_en_int(message.text)
    
    if note_number <= 0:
        await bale_bot.send_message(message.chat.id, MSG_INVALID_NUMBER, back_menu())
        return

    if not db_notes.check_is_exist(int(note_number)):
        message.author.del_state()
        await bale_bot.send_message(message.chat.id, MSG_NOTE_DOES_NOT_EXIST, back_menu())
        return

    if db_notes.is_note_sent(note_number):
        await bale_bot.send_message(message.chat.id, MSG_NOTE_SENT, back_menu())
        return

    user_temp_data[message.author.id] = {"note_edit_number": note_number}
    message.author.set_state("INPUT_EDIT_TEXT_NOTE")
    await bale_bot.send_message(message.chat.id, MSG_ENTER_NOTE_TEXT)


async def next_state_edit(message):
    user_id = message.author.id
    note_id = user_temp_data.get(user_id, {}).get("note_edit_number")

    try:
        db_notes.edit_content(note_id, message.text)
        await bale_bot.send_message(message.chat.id, MSG_NOTE_EDITED , back_menu())
    except Exception as e:
        await bale_bot.send_message(message.chat.id, str(e))

    user_temp_data.pop(user_id, None)
