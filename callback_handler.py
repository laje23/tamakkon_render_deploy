from config import *
from utils import set_schaduler_state, get_schaduler_state
import send_message_handler as _send


async def call_handler(callback_query):
    t = callback_query.data
    ci = callback_query.message.chat.id
    mi = callback_query.message.id
    ui = callback_query.author.id

    # 🏠 بازگشت به منوی اصلی
    if t == "back_to_main":
        await bale_bot.edit_message_text(
            ci, mi, "سلام! یکی از گزینه‌ها رو انتخاب کن:", main_menu(ui in admins)
        )

    elif t == "in_update":
        x = await _send.send_prayer("faraj")
        y = await _send.send_prayer("salavat")
        z = await _send.send_prayer("ahd")
        for i in [x, y, z]:
            await _send.send_to_debugger(i, True)

    # 📩 بازگشت به منوی پیام‌ها
    elif t == "back_to_message":
        try:
            callback_query.author.del_state()
        except:
            pass
        await bale_bot.edit_message_text(ci, mi, "منوی مدیریت پیام", message_menu())

    # 📤 منوی ارسال
    elif t == "send_menu":
        await bale_bot.edit_message_text(
            ci, mi, "لطفا یک گزینه برای ارسال انتخاب کنید", send_menu()
        )

    # 📝 منوی یادداشت‌ها
    elif t == "note_menu":
        await bale_bot.edit_message_text(
            ci, mi, "لطفا یک گزینه را انتخاب کنید", note_menu()
        )

    # 📚 منوی کتاب‌ها
    elif t == "book_menu":
        await bale_bot.edit_message_text(ci, mi, "منوی معرفی کتاب", book_menu())

    # 📊 دریافت آمار
    elif t == "get_status":
        book = db_books.get_status()
        clip = db_clips.get_status()
        hadith = db_hadith.get_status()
        note = db_notes.get_status()

        text = f"""آمار کلی سیستم:
.............................
کتاب‌ها
    ارسال شده: {book['sent']}
    ارسال نشده: {book['unsent']}

کلیپ‌ها
    ارسال شده: {clip['sent']}
    ارسال نشده: {clip['unsent']}

احادیث
    ارسال شده: {hadith['sent']}
    ارسال نشده: {hadith['unsent']}

یادداشت‌ها
    ارسال شده: {note['sent']}
    ارسال نشده: {note['unsent']}
"""
        await bale_bot.edit_message_text(ci, mi, text, back_menu())

    # 🔄 ارسال خودکار
    elif t == "auto_send_hadith":
        await bale_bot.edit_message_text(ci, mi, "در حال ارسال...")
        result = await _send.auto_send_hadith()
        await bale_bot.send_message(ci, result["message"], back_menu())

    elif t == "auto_send_note":
        await bale_bot.edit_message_text(ci, mi, "در حال ارسال...")
        result = await _send.auto_send_not()
        await bale_bot.send_message(ci, result["message"], back_menu())

    elif t == "auto_send_clip":
        result = await _send.send_auto_clip()
        await bale_bot.send_message(ci, result["message"], back_menu())

    elif t == "auto_send_book":
        result = await _send.send_auto_book()
        await bale_bot.send_message(ci, result["message"], back_menu())

    # 🧾 ذخیره یادداشت
    elif t == "save_note":
        callback_query.author.set_state("INPUT_NUMBER_NOTE")
        await bale_bot.send_message(ci, "شماره یادداشت رو وارد کنید", back_menu())

    # ✏️ ویرایش یادداشت
    elif t == "edit_note":
        callback_query.author.set_state("INPUT_EDIT_NUMBER_NOTE")
        await bale_bot.send_message(ci, "شماره یادداشت رو وارد کنید", back_menu())

    # 📚 ذخیره کتاب
    elif t == "save_book":
        callback_query.author.set_state("INPUT_BOOK_TITLE")
        await bale_bot.send_message(ci, "عنوان کتاب رو وارد کنید", back_menu())

    # ✏️ ویرایش کتاب
    elif t == "edit_book":
        callback_query.author.set_state("EDIT_BOOK_ID")
        await bale_bot.send_message(ci, "شناسه کتاب رو وارد کنید", back_menu())

    # 📤 ارسال پیام به کانال
    elif t == "send_to_channel":
        await bale_bot.send_message(ci, "پیام را ارسال یا فوروارد کنید")
        callback_query.author.set_state("SEND_MESSAGE_TO_CHANEL")

    elif t == "schaduler_menu":
        await bale_bot.edit_message_text(
            ci, mi, "وضعیت زمانبندی", schaduler_menu(on=get_schaduler_state())
        )

    elif t.startswith("schaduler"):
        if t == "schaduler_on":
            set_schaduler_state(True)
            await bale_bot.edit_message_text(ci, mi, "زمانبندی فعال شد", back_menu())

        elif t == "schaduler_off":
            set_schaduler_state(False)
            await bale_bot.edit_message_text(ci, mi, "زمانبندی غیرفعال شد", back_menu())


    elif t == "auto_send_lecture":
        result = await _send.send_auto_lecture()
        await bale_bot.send_message(ci, result["message"], back_menu())

