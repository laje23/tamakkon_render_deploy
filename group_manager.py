from config import db_hadith , db_notes, bot, bale_group_mirror_id, photo_url, process_hadith_message, process_note_message, bale_chanel_id
from send_message_handler import *



# manage group messages 

# hadith ............
async def save_hadith_message(chat_id , message_text ):
        id_ = db_hadith.give_hadith_id()
        try:
            await send_hadith_to_mirrors(id_ ,message_text )
        except Exception as e:
            await bot.send_message(chat_id, f"خطا در ارسال:\n{e}")


# hadith ..............................
async def handle_hadith_updats(chat_id , update_id , update_text ):
    result = db_hadith.select_finalid_by_baseid(update_id)
    if result:
        message_id, hadith_id = result
        try:
            await bot.edit_message_caption(bale_group_mirror_id, message_id, process_hadith_message(update_text, hadith_id))
        except Exception as e:
            await bot.send_message(chat_id, str(e))



# manage auto send message in channel ..........................................


# hadith ................................
async def send_auto_hadith():
    pass

# notes .............................
async def send_auto_note():
    msg_id = db_notes.select_note()
    if not msg_id:
        return "📭 تمام یادداشت‌ها ارسال شده‌اند."
    try:
        await bot.copy_message(bale_chanel_id, bale_group_mirror_id, msg_id)
        db_notes.sent_note_message(msg_id)
        return "✅ یادداشت با موفقیت ارسال شد."
    except Exception as e:
        return f"⛔️ خطا در ارسال یادداشت:\n{e}"



# send  hadith  by number ...............................


async def send_hadith_by_id(final_id):
    try: 
        await bot.copy_message(bale_chanel_id, bale_group_mirror_id, final_id)
        db_hadith.sent_message(final_id)
        return 'حدیث ارسال شد '
    except Exception as e :
        return e
    
    
    
    
    
