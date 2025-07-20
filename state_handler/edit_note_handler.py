from config import *



async def first_state_edit(message):
    if not message.text.isdigit() or int(message.text) <= 0:
        await bale_bot.send_message(message.chat.id, "❗️ لطفاً فقط عدد مثبت وارد کنید.", back_menu())
        return
    if not db_notes.chek_id_is_exist(int(message.text)):
        message.author.del_state()
        await bale_bot.send_message(message.chat.id , 'این یادداشت موجود نیست .آن را اول ایجاد کنید' , back_menu())
        return
        
    result = db_notes.select_message_id_by_id(message.text)
    if not result:
        await bale_bot.send_message(message.chat.id , 'یادداشت پیدا نشد. ' , back_menu())
        return
    note_message_id , sent = result 
    if sent == 1 :
        await bale_bot.send_message(message.chat.id , 'یادداشت ارسال شده است نمیتوان آن را ویرایش کرد. ' , back_menu())
        return 
    
    user_temp_data[message.author.id] = {"note_edit_number":(note_message_id , message.text )}
    
    message.author.set_state('INPUT_EDIT_TEXT_NOTE')
    await bale_bot.send_message(message.chat.id, " متن یادداشت رو بفرستید")
    
    
async def next_state_edit(message):
    user_id = message.author.id
    note_message_id ,note_id = user_temp_data.get(user_id, {}).get("note_edit_number")
    note_text = message.text
    
    
    try :
        await bale_bot.edit_message_text(group_mirror_id , note_message_id , process_note_message(note_text , note_id))
        await bale_bot.send_message(message.chat.id , 'ویرایش انجام شد' , back_menu())
    except Exception as e :
        await bale_bot.send_message(message.chat.id , str(e) , back_menu())