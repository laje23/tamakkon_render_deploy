from config import bot , back_menu , db_notes , group_mirror_id , process_note_message
user_temp_data = {}




async def first_step(message):
    if not message.text.isdigit() or int(message.text) <= 0:
        await bot.send_message(message.chat.id, "❗️ لطفاً فقط عدد مثبت وارد کنید.", back_menu())
        return
    
    user_temp_data[message.author.id] = {"note_number": message.text}
    
    message.author.set_state('INPUT_TEXT_NOTE')
    await bot.send_message(message.chat.id, "حالا متن یادداشت رو بفرست")
    
    
    
    
    
    
async def next_step(message):
    user_id = message.author.id
    note_number = user_temp_data.get(user_id, {}).get("note_number")

    if not note_number:
        await bot.send_message(message.chat.id, "شماره یادداشت پیدا نشد! دوباره امتحان کن." , back_menu())
        message.author.del_state()
        return

    note_text = message.text

    try :
        await bot.send_message(group_mirror_id , process_note_message(note_text , note_number))
        await db_notes.save_note(note_number ,  )
        await bot.send_message(message.chat.id, "یادداشت با موفقیت ذخیره شد ✅" , back_menu())
        message.author.del_state()
    except Exception as e :
        await bot.send_message(message.chat.id , str(e) , back_menu())
    # حذف از حافظه موقت
    user_temp_data.pop(user_id, None)