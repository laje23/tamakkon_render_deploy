from config import *
from app_manager import eitaa_manager



async def send_hadith_to_bale():
    
    hadith_id = db_hadith.select_random_hadith()
    if hadith_id:
        await bot.copy_message(bale_chanel_id, bale_group_mirror_id, hadith_id)
        db_hadith.sent_message(hadith_id)
        return "✅ حدیث ارسال شد."
    else :
        return "📚 همه احادیث ارسال شده‌اند."        



async def send_note_to_mirror_bale(id_note , text_note):
    """ -> bale_message_id """
    sent =await bot.send_message(bale_group_mirror_id , process_note_message(text_note , id_note))
    if sent :
        return sent.id if sent else None

async def send_note_to_mirror_eitaa(id_note , text_note):
    """ -> eitaa_message_id """
    sent = await eitaa_manager.send_text_to_group(eitaa_group_mirror_id , process_note_message(text_note , id_note))
    return sent['result']['message_id'] if sent['ok'] else 'false'
    

async def send_note_to_mirrors(hadith_id, note_text):

    bale_mesage_id = await send_note_to_mirror_bale(hadith_id , note_text)
    eitaa_message_id = await send_note_to_mirror_eitaa(hadith_id , note_text)
    if bale_mesage_id and eitaa_message_id :
        db_notes.save_note_ids(hadith_id , bale_mesage_id , eitaa_message_id)
    
    
    
    
async def send_hadith_to_mirror_eitaa(id_hadith , text_hadith):
    sent = await eitaa_manager.send_file_to_group(eitaa_group_mirror_id , photo_url , process_hadith_message(text_hadith , id_hadith))
    return sent['result']['message_id'] if sent['ok'] else 'false'
        
async def send_hadith_to_mirror_bale(id_hadith , text_hadith):
    with open(photo_url , 'rb') as photo :
        sent = await bot.send_photo(bale_group_mirror_id , photo , process_hadith_message(text_hadith , id_hadith))
    return sent.id if sent else None


async def send_hadith_to_mirrors(hadith_id , hadith_text):
    try :
        bale_mesage_id = await send_hadith_to_mirror_bale(hadith_id , hadith_text)
        eitaa_message_id = await send_hadith_to_mirror_eitaa(hadith_id , hadith_text)
        if bale_mesage_id and eitaa_message_id :
            db_hadith.save_hadith_ids(hadith_id , bale_mesage_id , eitaa_message_id)
    except Exception as e :
        print (e)