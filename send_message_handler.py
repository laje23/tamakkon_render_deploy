from config import * 
import io 
from utils import *



async def auto_send_hadith():
    content , id = db_hadith.return_auto_content()
    text = process_hadith_message(content , id )
    try :
        with open (photo_url , 'rb') as photo:
            await bale_bot.send_photo(bale_channel_id , photo , text )
            await eitaa_bot.send_file(eitaa_channel_id , photo , text)
            await gap_bot.send_file()
        db_hadith.mark_sent(id)
        return 'پیام ارسال شد'
    except Exception as e :
        return f'پیام ارسال نشد \n ارور :\n {e} '
    
    
    
async def auto_send_not():
    content , id = db_notes.auto_return_content()
    text = process_note_message(content , id )
    try:
        await bale_bot.send_message(bale_channel_id , text)
        await eitaa_bot.send_message(eitaa_channel_id , text)
        db_notes.mark_sent(id)
        return 'پیام ارسال شد '
    except Exception as e :
        return f'پیام ارسال نشد \n ارور :\n {e} '
    
    
async def send_message_to_channel(message , bot):
        if (x := await get_photo_bytes(message, bot)):
            try:
                await bale_bot.send_photo(bale_channel_id , x , message.caption )
                await eitaa_bot.send_file(eitaa_channel_id , x , message.caption)
                return "پیام ارسال شد"
            except Exception as e :
                return f"خطا در ارسال پیام {e}"
        else :
            try :
                await bale_bot.send_message(bale_channel_id , message.text)
                await eitaa_bot.send_message(eitaa_channel_id , message.text)
                return "پیام ارسال شد "
            except Exception as e :
                return f"خطا در ارسال پیام {e}"
            