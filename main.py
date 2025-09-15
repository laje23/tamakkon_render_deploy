from balethon.conditions import command, group, at_state, private, all
from config import *
from state_handler import *
from callback_handler import call_handler
from dotenv import load_dotenv
from utils import error_response
from send_message_handler import send_message_to_channel, send_to_debugger
from schaduler import scheduled_messages
import threading

load_dotenv()


# 🎯 هندل کردن دکمه‌های callback
@bale_bot.on_callback_query(private)
async def reply_buttons(callback_query):
    await call_handler(callback_query)


# 🚀 شروع ربات
@bale_bot.on_message(command("start") & private)
async def handle_start(message):
    is_admin = message.author.id in admins
    await bale_bot.send_message(
        message.chat.id,
        "سلام! یکی از گزینه‌ها رو انتخاب کنید:",
        main_menu(is_admin),
    )


# 📝 ذخیره یادداشت
@bale_bot.on_message(at_state("INPUT_NUMBER_NOTE"))
async def first_state_save_note(message):
    await first_step_save(message)


@bale_bot.on_message(at_state("INPUT_TEXT_NOTE"))
async def next_state_save_note(message):
    await next_step_save(message)


# ✏️ ویرایش یادداشت
@bale_bot.on_message(at_state("INPUT_EDIT_NUMBER_NOTE"))
async def first_state_edit_note(message):
    await first_state_edit(message)


@bale_bot.on_message(at_state("INPUT_EDIT_TEXT_NOTE"))
async def next_state_edit_note(message):
    await next_state_edit(message)


# 📢 ارسال پیام به کانال
@bale_bot.on_message(at_state("SEND_MESSAGE_TO_CHANEL") & all)
async def send_to_channel(message):
    sent = await bale_bot.send_message(message.chat.id, "در حال ارسال ...")
    text = await send_message_to_channel(message, bale_bot)
    message.author.del_state()
    await bale_bot.edit_message_text(sent.chat.id, sent.id, text, back_menu())


@bale_bot.on_message(at_state("INPUT_BOOK_TITLE"))
async def handle_book_title(message):
    await input_book_title(message)


@bale_bot.on_message(at_state("INPUT_BOOK_AUTHOR"))
async def handle_book_author(message):
    await input_book_author(message)


@bale_bot.on_message(at_state("INPUT_BOOK_PUBLISHER"))
async def handle_book_publisher(message):
    await input_book_publisher(message)


@bale_bot.on_message(at_state("INPUT_BOOK_EXCERPT"))
async def handle_book_excerpt(message):
    await input_book_excerpt(message)


@bale_bot.on_message(at_state("EDIT_BOOK_ID"))
async def handle_book_id_edit(message):
    await input_book_id_for_edit(message)


@bale_bot.on_message(at_state("EDIT_BOOK_TITLE"))
async def handle_book_title_edit(message):
    await input_new_title(message)


@bale_bot.on_message(at_state("EDIT_BOOK_AUTHOR"))
async def handle_book_author_edit(message):
    await input_new_author(message)


@bale_bot.on_message(at_state("EDIT_BOOK_PUBLISHER"))
async def handle_book_publisher_edit(message):
    await input_new_publisher(message)


@bale_bot.on_message(at_state("EDIT_BOOK_EXCERPT"))
async def handle_book_excerpt_edit(message):
    await input_new_excerpt(message)


# 📥 دریافت پیام‌های گروهی
@bale_bot.on_message(group)
async def collect_group_input(message):
    try:
        if message.chat.id == group_reserch_hadith_id:
            db_hadith.save_id_and_content(message.id, message.text)

        elif message.chat.id == group_reserch_clip_id and message.video:
            if message.video :
                db_clips.save_clip(message.video.id, message.caption)
            else :
                await send_to_debugger(error_response('پیام ارسال شده در گروه کلیپ فرمتی نامعتبر دارد'))
            
        elif message.chat.id == group_reserch_lecture_id :
            if message.audio :
                db_lecture.save_lecture(message.audio.id , message.caption)            
            else :
                await send_to_debugger(error_response('پیام ارسال شده در گروه سخنرانی فرمتی نامعتبر دارد'))

    except Exception as e:
        await send_to_debugger(e)


# ⏰ اجرای پیام‌های زمان‌بندی‌شده
def start_scheduler_loop():
    asyncio.run(scheduled_messages())


threading.Thread(target=start_scheduler_loop, daemon=True).start()

# 🧠 اجرای اصلی ربات
bale_bot.run()
