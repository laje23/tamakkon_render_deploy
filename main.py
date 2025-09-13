from balethon.conditions import command, group, at_state, private, all , video
from config import *
from state_handler import *
from callback_handler import call_handler
from dotenv import load_dotenv
from send_message_handler import send_message_to_channel , send_to_debugger
from models import clips
from schaduler import scheduled_messages


load_dotenv()
@bale_bot.on_callback_query(private)
async def reply_buttons(callback_query):
    await call_handler(callback_query)


@bale_bot.on_message(command("start") & private)
async def handle_start(message):
    await bale_bot.send_message(
        message.chat.id,
        "سلام! یکی از گزینه‌ها رو انتخاب کنید:",
        main_menu(message.author.id in admins),
    )


@bale_bot.on_message(at_state("INPUT_NUMBER_NOTE"))
async def first_state_save_note(message):
    await first_step_save(message)


@bale_bot.on_message(at_state("INPUT_TEXT_NOTE"))
async def next_state_save_note(message):
    await next_step_save(message)


@bale_bot.on_message(at_state("INPUT_EDIT_NUMBER_NOTE"))
async def first_state_edit_not(message):
    await first_state_edit(message)


@bale_bot.on_message(at_state("INPUT_EDIT_TEXT_NOTE"))
async def next_state_edit_not(message):
    await next_state_edit(message)


@bale_bot.on_message(at_state("SEND_MESSAGE_TO_CHANEL") & all)
async def send_to_chanle(message):
    sent = await bale_bot.send_message(message.chat.id, "در حال ارسال ...")
    text = await send_message_to_channel(message, bale_bot)
    message.author.del_state()
    await bale_bot.edit_message_text(sent.chat.id, sent.id, text, back_menu())


@bale_bot.on_message(group)
async def collect_group_input(message):
    if message.chat.id == group_reserch_hadith_id:
        try:
            db_hadith.save_id_and_content(message.id, message.text)
        except Exception as e :
            await send_to_debugger(e)
    
    elif message.chat.id == group_reserch_clip_id :
        if message.video :
            file_id = message.video.id 
            caption = message.caption 
            try :
                clips.save_file_id(file_id , caption )
            except Exception as e:
                await send_to_debugger(e)

def start_scheduler_loop():
    asyncio.run(scheduled_messages())


# اجرای scheduler در یک ترد جدا
threading.Thread(target=start_scheduler_loop, daemon=True).start()

# اجرای ربات (که معمولاً متد run بلوک‌کننده است)
bale_bot.run()


