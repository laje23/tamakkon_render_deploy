from config import *



async def first_state_edit(message):
    if not message.text.isdigit() or int(message.text) <= 0:
        await bot.send_message(message.chat.id, "❗️ لطفاً فقط عدد مثبت وارد کنید.", back_menu())
        return
    if not db_notes.chek_id_is_exist(int(message.text)):
        message.author.del_state()
        await bot.send_message(message.chat.id , 'این یادداشت موجود نیست .آن را اول ایجاد کنید' , back_menu())
        return
        
    
    user_temp_data[message.author.id] = {"note_edit_number": message.text}
    
    message.author.set_state('INPUT_EDIT_TEXT_NOTE')
    await bot.send_message(message.chat.id, " متن یادداشت رو بفرستید")
    
    
async def next_state_edit(message):
    user_id = message.author.id
    note_id = user_temp_data.get(user_id, {}).get("note_edit_number")
    note_text = message.text
    
    note_message_id =db_notes.select_message_id_by_id(note_id)
    try :
        await bot.edit_message_text(group_mirror_id , note_message_id , process_note_message(note_text , note_id))
        await bot.send_message(message.chat.id , 'ویرایش انجام شد' , back_menu())
    except Exception as e :
        await bot.send_message(message.chat.id , str(e) , back_menu())