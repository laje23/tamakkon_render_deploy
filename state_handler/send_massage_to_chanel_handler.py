from config import bot , chanel_tamakkon_id , back_menu



async def send_message_to_chanel(message):
    try :
        await bot.copy_message(chanel_tamakkon_id , message.chat.id , message.id )
        message.author.del_state()
        await bot.send_message(message.chat.id , 'پیام ارسال شد ' , back_menu())
    except Exception as e:
        await bot.send_message(message.chat.id ,str(e) , back_menu())
        message.author.del_state()