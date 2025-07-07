from balethon.conditions import command, group, at_state, private, equals
from config import *  
from group_manager import *


# todo ...............................
@bot.on_callback_query(private)
async def reply_buttons(callback_query):
    t = callback_query.data
    ci = callback_query.message.chat.id
    mi = callback_query.message.id
    
    if t == 'back_to_main':
        await bot.edit_message_text(ci ,mi ,"سلام! یکی از گزینه‌ها رو انتخاب کن:" , main_menu(True))
    
    elif t == 'back_to_message':
        try:
            callback_query.message.author.del_state()
        except :
            pass
        await bot.edit_message_text(ci ,mi ,'منوی مدیریت پیام' , message_menu() )
        
    elif t == 'menu_hadith':
        await bot.edit_message_text(ci ,mi ,'لطفا یک گزینه برای ارسال انتخاب کنید' , hadith_menu() )
        
    elif t == 'send_note':
        text = await send_auto_note()
        await bot.edit_message_text(ci , mi, text , back_menu())
    
    elif t == 'send_random_hadith':
        text = await send_auto_hadith()
        await bot.edit_message_text(ci ,mi ,  text , back_menu())

    elif t == 'get_stats':
        total=  get_state()
        await bot.edit_message_text(ci , mi, total , back_menu())
    
    elif t == 'send_hadith_by_number':
        callback_query.message.author.set_state('INPUT_NUMBER')
        await bot.send_message(ci , 'شماره حدیث رو وارد کنید' , back_menu())
        
        
    elif t.startswith('resend:'):
        callback_query.message.author.del_state()
        msg_id = int(t.split(":")[1])
        text = await send_hadith_by_id(msg_id , ci , mi)
        await bot.edit_message_text(ci ,mi ,text, back_menu())


@bot.on_message(command("start") & private)
async def handle_start(message):
    await bot.send_message(message.chat.id, "سلام! یکی از گزینه‌ها رو انتخاب کن:", main_menu(True))


# 🎯 دریافت شماره حدیث از ریپلای


@bot.on_message(at_state("INPUT_NUMBER"))
async def handle_hadith_id(message):
    if not message.text.isdigit() and  int(message.text)<= 0:
        await bot.send_message(message.chat.id, "❗️ لطفاً فقط عدد وارد کنید.")
        return

    try:
        result = db_hadith.select_hadith_by_id(int(message.text))
        if not result:
            await bot.send_message(message.chat.id, "❌ حدیث یافت نشد." , back_menu())
            return

        msg_id, sent = result
        if sent == 1:
            await message.reply("این حدیث قبلاً ارسال شده است ❗. اگر مایل به ارسال دوباره آن هستید روی شناسه آن کلیک کنید", answer_y_n(msg_id))
            return

        await bot.copy_message(chanel_tamakkon_id, group_mirror_id, msg_id)
        db_hadith.sent_message(msg_id)
        await bot.send_message(message.chat.id, "✅ حدیث ارسال شد." , back_menu())
        message.author.del_state()
    except Exception as e:
        await bot.send_message(message.chat.id, f"⚠️ خطا:\n{e}")

@bot.on_message(private)
async def handle_answer(message):
    try:
        message_id = int(message.text)
        await bot.copy_message(chanel_tamakkon_id, group_mirror_id, message_id)
        db_hadith.sent_message(message_id)
        await bot.send_message(message.chat.id, "✅ حدیث ارسال شد", back_menu())
    except ValueError:
        pass
    except Exception as e:
        await bot.send_message(message.chat.id, str(e))
        message.author.del_state()


@bot.on_message(group)
async def collect_group_input(message):
    if message.chat.id == group_pajohesh_hadith_id:
        await manage_hadith_message(message.chat.id , message.id , message.text)

    elif message.chat.id == group_pajohesh_notes_id:
        await manage_notes_message(message.chat.id , message.id , message.text)
        

@bot.on_update()
async def update_handler(update):
    if update.chat.id == group_pajohesh_hadith_id:
        await handle_hadith_updats(update.chat.id , update.id , update.text)

    elif update.chat.id == group_pajohesh_notes_id:
        await handle_notes_updats(update.chat.id , update.id , update.text)
        


bot.run()
