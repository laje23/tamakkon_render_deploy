from config import db_hadith , db_notes, bot, group_mirror_id, photo_url, process_hadith_message, process_note_message, chanel_tamakkon_id




# manage group messages 

# hadith ............
async def manage_hadith_message(chat_id , message_id , message_text ):
        id_ = db_hadith.save_base_hadith_id(message_id)
        try:
            sent = await bot.send_photo(group_mirror_id, photo_url, process_hadith_message(message_text, id_))
            db_hadith.save_final_hadith_id(sent.id, id_)
        except Exception as e:
            db_hadith.delete_base_hadith_by_id(message_id)
            await bot.send_message(chat_id, f"خطا در ارسال:\n{e}")

# notes ..............
# async def manage_notes_message(chat_id , message_id , message_text ):
#         note_id = db_notes.save_note_id(message_id)
#         try:
#             sent = await bot.send_message(group_mirror_id, process_note_message(message_text, note_id))
#             db_notes.save_final_note_id(sent.id, note_id)
#         except Exception as e:
#             await bot.send_message(chat_id, f"خطا در ارسال:\n{e}")



# handle updatas .................................................


# hadith ..............................
async def handle_hadith_updats(chat_id , update_id , update_text ):
    result = db_hadith.select_finalid_by_baseid(update_id)
    if result:
        message_id, hadith_id = result
        try:
            await bot.edit_message_caption(group_mirror_id, message_id, process_hadith_message(update_text, hadith_id))
        except Exception as e:
            await bot.send_message(chat_id, str(e))


# notes ................................
async def handle_notes_updats(chat_id , update_id , update_text ):
    result = db_notes.select_final_note_by_base(update_id)
    if result:
        message_id, note_id = result
        try:
            await bot.edit_message_text(group_mirror_id, message_id, process_note_message(update_text, note_id))
        except Exception as e:
            await bot.send_message(chat_id, str(e))



# manage auto send message in channel ..........................................


# hadith ................................
async def send_auto_hadith():
    try:
        hadith_id = db_hadith.select_random_hadith()
        if hadith_id:
            await bot.copy_message(chanel_tamakkon_id, group_mirror_id, hadith_id)
            db_hadith.sent_message(hadith_id)
            return "✅ حدیث ارسال شد."
        else :
            return "📚 همه احادیث ارسال شده‌اند."
    except Exception as e:
        return f"⛔️ خطا در ارسال حدیث:\n{e}"

# notes .............................
async def send_auto_note():
    msg_id = db_notes.select_note()
    if not msg_id:
        return "📭 تمام یادداشت‌ها ارسال شده‌اند."
    try:
        await bot.copy_message(chanel_tamakkon_id, group_mirror_id, msg_id)
        db_notes.sent_note_message(msg_id)
        return "✅ یادداشت با موفقیت ارسال شد."
    except Exception as e:
        return f"⛔️ خطا در ارسال یادداشت:\n{e}"



# send  hadith  by number ...............................


async def send_hadith_by_id(final_id , chat_id , message_id):
    try: 
        await bot.copy_message(chanel_tamakkon_id, group_mirror_id, final_id)
        db_hadith.sent_message(final_id)
        return 'حدیث ارسال شد '
    except Exception as e :
        return e
    
    
    
    
    
