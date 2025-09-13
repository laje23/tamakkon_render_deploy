from config import bale_bot, back_menu, user_temp_data
from models.books import (
    save_book,
    check_book_exists,
    get_unsent_book,
    edit_book,  # فرض بر اینه که این تابع در models.books تعریف شده
)

# 📌 پیام‌های ثابت
MSG_ENTER_TITLE = "عنوان کتاب رو وارد کن:"
MSG_ENTER_AUTHOR = "نام نویسنده کتاب رو وارد کن:"
MSG_ENTER_PUBLISHER = "نام ناشر رو وارد کن (یا بنویس «ندارم»):"
MSG_ENTER_EXCERPT = "گزیده‌ای از کتاب رو وارد کن (یا بنویس «ندارم»):"
MSG_BOOK_SAVED = "✅ کتاب با موفقیت ذخیره شد."
MSG_BOOK_ERROR = "❌ خطا در ذخیره کتاب: "

MSG_ENTER_BOOK_ID = "شناسه کتابی که می‌خوای ویرایش کنی رو وارد کن:"
MSG_BOOK_NOT_FOUND = "❌ کتابی با این شناسه پیدا نشد."
MSG_BOOK_ALREADY_SENT = "این کتاب قبلاً ارسال شده و قابل ویرایش نیست."
MSG_ENTER_NEW_TITLE = "عنوان جدید کتاب رو وارد کن:"
MSG_ENTER_NEW_AUTHOR = "نام نویسنده جدید رو وارد کن:"
MSG_ENTER_NEW_PUBLISHER = "نام ناشر جدید رو وارد کن (یا بنویس «ندارم»):"
MSG_ENTER_NEW_EXCERPT = "گزیده جدید رو وارد کن (یا بنویس «ندارم»):"
MSG_BOOK_EDITED = "✅ کتاب با موفقیت ویرایش شد."
MSG_BOOK_EDIT_ERROR = "❌ خطا در ویرایش کتاب: "


# 🟢 ثبت کتاب جدید

async def input_book_title(message):
    user_id = message.author.id
    user_temp_data[user_id] = {"title": message.text.strip()}
    message.author.set_state("INPUT_BOOK_AUTHOR")
    await bale_bot.send_message(message.chat.id, MSG_ENTER_AUTHOR)


async def input_book_author(message):
    user_id = message.author.id
    user_temp_data[user_id]["author"] = message.text.strip()
    message.author.set_state("INPUT_BOOK_PUBLISHER")
    await bale_bot.send_message(message.chat.id, MSG_ENTER_PUBLISHER)


async def input_book_publisher(message):
    user_id = message.author.id
    publisher = None if message.text.strip() == "ندارم" else message.text.strip()
    user_temp_data[user_id]["publisher"] = publisher
    message.author.set_state("INPUT_BOOK_EXCERPT")
    await bale_bot.send_message(message.chat.id, MSG_ENTER_EXCERPT)


async def input_book_excerpt(message):
    user_id = message.author.id
    excerpt = None if message.text.strip() == "ندارم" else message.text.strip()
    data = user_temp_data.get(user_id, {})

    try:
        save_book(
            title=data.get("title"),
            author=data.get("author"),
            publisher=data.get("publisher"),
            excerpt=excerpt,
        )
        await bale_bot.send_message(message.chat.id, MSG_BOOK_SAVED, back_menu())
    except Exception as e:
        await bale_bot.send_message(message.chat.id, f"{MSG_BOOK_ERROR}{str(e)}", back_menu())

    user_temp_data.pop(user_id, None)
    message.author.del_state()


# ✏️ ویرایش کتاب موجود

async def input_book_id_for_edit(message):
    book_id_text = message.text.strip()
    if not book_id_text.isdigit():
        await bale_bot.send_message(message.chat.id, "لطفاً فقط عدد وارد کن.", back_menu())
        return

    book_id = int(book_id_text)
    if not check_book_exists(book_id):
        await bale_bot.send_message(message.chat.id, MSG_BOOK_NOT_FOUND, back_menu())
        message.author.del_state()
        return

    book = get_unsent_book()
    if not book or book["id"] != book_id:
        await bale_bot.send_message(message.chat.id, MSG_BOOK_ALREADY_SENT, back_menu())
        message.author.del_state()
        return

    user_temp_data[message.author.id] = {"edit_book_id": book_id}
    message.author.set_state("EDIT_BOOK_TITLE")
    await bale_bot.send_message(message.chat.id, MSG_ENTER_NEW_TITLE)


async def input_new_title(message):
    user_id = message.author.id
    user_temp_data[user_id]["title"] = message.text.strip()
    message.author.set_state("EDIT_BOOK_AUTHOR")
    await bale_bot.send_message(message.chat.id, MSG_ENTER_NEW_AUTHOR)


async def input_new_author(message):
    user_id = message.author.id
    user_temp_data[user_id]["author"] = message.text.strip()
    message.author.set_state("EDIT_BOOK_PUBLISHER")
    await bale_bot.send_message(message.chat.id, MSG_ENTER_NEW_PUBLISHER)


async def input_new_publisher(message):
    user_id = message.author.id
    publisher = None if message.text.strip() == "ندارم" else message.text.strip()
    user_temp_data[user_id]["publisher"] = publisher
    message.author.set_state("EDIT_BOOK_EXCERPT")
    await bale_bot.send_message(message.chat.id, MSG_ENTER_NEW_EXCERPT)


async def input_new_excerpt(message):
    user_id = message.author.id
    excerpt = None if message.text.strip() == "ندارم" else message.text.strip()
    data = user_temp_data.get(user_id, {})
    book_id = data.get("edit_book_id")

    try:
        edit_book(
            book_id=book_id,
            title=data.get("title"),
            author=data.get("author"),
            publisher=data.get("publisher"),
            excerpt=excerpt,
        )
        await bale_bot.send_message(message.chat.id, MSG_BOOK_EDITED, back_menu())
    except Exception as e:
        await bale_bot.send_message(message.chat.id, f"{MSG_BOOK_EDIT_ERROR}{str(e)}", back_menu())

    user_temp_data.pop(user_id, None)
    message.author.del_state()
