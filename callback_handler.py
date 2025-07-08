
from config import *
from group_manager import *



async def call_handler(callback_query):
    t = callback_query.data
    ci = callback_query.message.chat.id
    mi = callback_query.message.id
    
    if t == 'back_to_main':
        await bot.edit_message_text(ci ,mi ,"سلام! یکی از گزینه‌ها رو انتخاب کن:" , main_menu(True))
    
    elif t == 'back_to_message':
        try:
            callback_query.author.del_state()
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
    
    elif t.startswith('resend:'):
        callback_query.author.del_state()
        msg_id = int(t.split(":")[1])
        text = await send_hadith_by_id(msg_id , ci , mi)
        await bot.edit_message_text(ci ,mi ,text, back_menu())
    
    elif t == 'send_hadith_by_number':
        await bot.send_message(ci , 'شماره حدیث رو وارد کنید' , back_menu())
        callback_query.author.set_state('INPUT_NUMBER_HADITH')
        
    elif t == 'save_note':
        await bot.send_message(ci, 'شماره یادداشت رو وارد کنید' , back_menu())
        callback_query.author.set_state('INPUT_NUMBER_NOTE')
        
    elif t == 'edit_note' :
        await bot.send_message(ci , 'لطفا شماره یادداشت رو وارد کنید' , back_menu())
        callback_query.author.set_state('INPUT_EDIT_NUMBER_NOTE')