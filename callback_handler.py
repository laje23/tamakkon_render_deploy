
from config import *
import send_message_handler as _send

# from send_message_handler import auto_send_note_to_channels

async def call_handler(callback_query):
    t = callback_query.data
    ci = callback_query.message.chat.id
    mi = callback_query.message.id
    ui = callback_query.author.id
    
    if t == 'back_to_main':
        await bale_bot.edit_message_text(ci ,mi ,"سلام! یکی از گزینه‌ها رو انتخاب کن:" , main_menu(ui in admins))
    
    elif t == 'back_to_message':
        try:
            callback_query.author.del_state()
        except :
            pass
        await bale_bot.edit_message_text(ci ,mi ,'منوی مدیریت پیام' , message_menu() )
        
    elif t == 'hadith_menu':
        await bale_bot.edit_message_text(ci ,mi ,'لطفا یک گزینه برای ارسال انتخاب کنید' , hadith_menu() )
    
    elif t == 'note_menu':
        await bale_bot.edit_message_text(ci ,mi ,'لطفا یک گزینه را انتخاب کنید' , note_menu() )
    
    
    elif t == 'auto_send_hadith':
        await bale_bot.edit_message_text(ci ,mi , 'در حال ارسال...')
        text = await _send.auto_send_hadith()
        await bale_bot.edit_message_text(ci ,mi ,  text , back_menu())

    elif t == 'get_stats':
        pass
        total=  get_state()
        await bale_bot.edit_message_text(ci , mi, total , back_menu())

    elif t == 'auto_send_note':
        await bale_bot.edit_message_text(ci ,mi , 'در حال ارسال...')
        text = await _send.auto_send_not()
        await bale_bot.edit_message_text(ci ,mi ,  text , back_menu())
        
    elif t == 'save_note':
        callback_query.author.set_state('INPUT_NUMBER_NOTE')
        await bale_bot.send_message(ci, 'شماره یادداشت رو وارد کنید' , back_menu())
    elif t == "edit_note":
        callback_query.author.set_state('INPUT_EDIT_NUMBER_NOTE')
        await bale_bot.send_message(ci, 'شماره یادداشت رو وارد کنید' , back_menu())
        
    elif t == 'send_to_channel':
        await bale_bot.send_message(ci , 'پیام را ارسال یا فوروارد کنید ')
        callback_query.author.set_state('SEND_MESSAGE_TO_CHANEL')
    
    elif t == 'send_laftovers':
        hadith= await _send.send_laftover_hadith()
        note = await _send.send_laftover_note()
        await bale_bot.edit_message_text(ci ,mi , f'حدیث ها \n {hadith} \n\n یادداشت ها \n {note}' , back_menu())
        
