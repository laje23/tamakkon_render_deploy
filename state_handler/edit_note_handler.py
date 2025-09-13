from config import *


async def first_state_edit(message):
    if not message.text.isdigit() or int(message.text) <= 0:
        await bale_bot.send_message(
            message.chat.id, "❗️ لطفاً فقط عدد مثبت وارد کنید.", back_menu()
        )
        return
    if not db_notes.chek_is_exist(int(message.text)):
        message.author.del_state()
        await bale_bot.send_message(
            message.chat.id, "این یادداشت موجود نیست .آن را اول ایجاد کنید", back_menu()
        )
        return

    bale, eitaa = db_notes.return_sent(message.text)

    if bale == 1 or eitaa == 1:
        await bale_bot.send_message(
            message.chat.id,
            "یادداشت ارسال شده است نمیتوان آن را ویرایش کرد. ",
            back_menu(),
        )
        return

    user_temp_data[message.author.id] = {"note_edit_number": (message.text)}

    message.author.set_state("INPUT_EDIT_TEXT_NOTE")
    await bale_bot.send_message(message.chat.id, " متن یادداشت رو بفرستید")


async def next_state_edit(message):
    user_id = message.author.id
    note_id = user_temp_data.get(user_id, {}).get("note_edit_number")
    note_text = message.text
    try:
        db_notes.edit_content(note_id, note_text)
        await bale_bot.send_message(message.chat.id, "یادداشت ویرایش شد")
    except Exception as e:
        await bale_bot.send_message(message.chat.id, str(e))
