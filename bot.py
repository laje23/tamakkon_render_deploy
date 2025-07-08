from balethon.conditions import command, group, at_state, private, equals
from config import *  
from group_manager import *
from state_handler.save_note_handler import *
from state_handler.send_hadith_handler import *


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
        
    elif t == 'hadith_menu':
        await bot.edit_message_text(ci ,mi ,'لطفا یک گزینه برای ارسال انتخاب کنید' , hadith_menu() )
    
    elif t == 'note_menu':
        await bot.edit_message_text(ci ,mi ,'لطفا یک گزینه را انتخاب کنید' , note_menu() )
    
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
        callback_query.message.author.set_state('INPUT_NUMBER_HADITH')
        await bot.send_message(ci , 'شماره حدیث رو وارد کنید' , back_menu())
        
    elif t == 'save_note':
        callback_query.message.author.set_state('INPUT_NUMBER_NOTE')
        await bot.send_message(ci, 'شماره یادداشت رو وارد کنید' , back_menu())
        
        
    elif t.startswith('resend:'):
        callback_query.message.author.del_state()
        msg_id = int(t.split(":")[1])
        text = await send_hadith_by_id(msg_id , ci , mi)
        await bot.edit_message_text(ci ,mi ,text, back_menu())


@bot.on_message(command("start") & private)
async def handle_start(message):
    await bot.send_message(message.chat.id, "سلام! یکی از گزینه‌ها رو انتخاب کنید:", main_menu(True))


# 🎯 دریافت شماره حدیث از ریپلای


@bot.on_message(at_state("INPUT_NUMBER_HADITH"))
async def handle_hadith_id(message):
    await handel_number_hadith(message)


@bot.on_message(private & at_state('INPUT_NUMBER_NOTE')) 
async def first_state_save_note(message):
    await first_step(message)

@bot.on_message(at_state('INPUT_TEXT_NOTE'))
async def next_state_save_note(message):
    await next_step(message)    



@bot.on_message(group)
async def collect_group_input(message):
    if message.chat.id == group_pajohesh_hadith_id:
        await manage_hadith_message(message.chat.id , message.id , message.text)

@bot.on_edited_message()
async def update_handler(message):
    if message.chat.id == group_pajohesh_hadith_id:
        await handle_hadith_updats(message.chat.id , message.id , message.text)

        


bot.run()
