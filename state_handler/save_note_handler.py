from config import bale_bot , back_menu , db_notes  , process_note_message , user_temp_data , edit_menu

# from send_message_handler import send_note_to_mirrors


async def first_step_save(message):
    if not message.text.isdigit() or int(message.text) <= 0:
        await bale_bot.send_message(message.chat.id, "❗️ لطفاً فقط عدد مثبت وارد کنید.", back_menu())
        return
    
    if db_notes.chek_is_exist(int(message.text)):
        message.author.del_state()
        await bale_bot.send_message(message.chat.id , 'این یادداشت موجود است . میخواهید آن را ویرایش کنید' , edit_menu())
        return
    
    
    user_temp_data[message.author.id] = {"note_number": message.text}
    
    message.author.set_state('INPUT_TEXT_NOTE')
    await bale_bot.send_message(message.chat.id, " متن یادداشت رو بفرستید")
    
    
    
    
    
    
async def next_step_save(message):
    user_id = message.author.id
    note_number = user_temp_data.get(user_id, {}).get("note_number")

    if not note_number:
        await bale_bot.send_message(message.chat.id, "شماره یادداشت پیدا نشد! دوباره امتحان کن." , back_menu())
        message.author.del_state()
        return

    note_text = message.text

    try :
        db_notes.new_note(note_number , note_text)
        await bale_bot.send_message(message.chat.id , 'یادداشت با موفقیت ذخیره شد ' , back_menu())
    except Exception as e :
        await bale_bot.send_message(message.chat.id , str(e) , back_menu())
    # حذف از حافظه موقت
    user_temp_data.pop(user_id, None)