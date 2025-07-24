from config import * 
from utils import *
import asyncio
async def send_to_debuger(err_text):
    if err_text and not err_text == 'پیام ارسال شد':
        await bale_bot.send_message(debuger_id , err_text)



async def auto_send_hadith():
    result = db_hadith.return_auto_content()
    if not result:
        return 'هیچ پیامی موجود نیست'
    
    content, id = result
    text = process_hadith_message(content, id)
    
    if not os.path.exists(photo_url):
        return f'عکس موجود نیست: {photo_url}'
    
    try:
        with open(photo_url, 'rb') as photo:
            bale_task = bale_bot.send_photo(bale_channel_id, photo, text)
            eitaa_task = eitaa_bot.send_file(eitaa_channel_id, photo, text)
            bale, eitaa = await asyncio.gather(bale_task, eitaa_task)
        
        if bale and eitaa:
            db_hadith.mark_sent_all(id)
            return 'پیام ارسال شد'
        elif bale and not eitaa:
            db_hadith.mark_sent_bale(id)
            return "پیام در ایتا ارسال نشد"
        elif not bale and eitaa:
            db_hadith.mark_sent_eitaa(id)
            return "پیام در بله ارسال نشد"
        else:
            return 'پیام در هیچ یک ارسال نشد'
        
    except Exception as e:
        return f'پیام ارسال نشد \n ارور :\n {e}'
    
    
    
async def auto_send_not():
    result = db_notes.auto_return_content()
    if not result :
        return 'هیچ پیامی موجود نیست'
    content , id = result
    text = process_note_message(content , id )
    try:
        bale = await bale_bot.send_message(bale_channel_id , text)
        eitaa =await eitaa_bot.send_message(eitaa_channel_id , text)
        if bale and eitaa :
            db_notes.mark_sent_all(id)
        elif bale :
            db_notes.mark_sent_bale(id)
        elif eitaa :
            db_notes.mark_sent_eitaa(id)
        
        
        return 'پیام ارسال شد'
    except Exception as e :
        return f'پیام ارسال نشد \n ارور :\n {e} '
    
    
async def send_message_to_channel(message , bot):
        if (x := await get_media_bytes(message, bot)):
            bin_file , typefile = x 
            try:
                if typefile == 'photo' :
                    await bale_bot.send_photo(bale_channel_id , bin_file , message.caption )
                elif typefile == 'video':
                    await bale_bot.send_video(bale_channel_id , bin_file , message.caption )
                elif typefile == 'voice':
                    await bale_bot.send_voice(bale_channel_id , bin_file , message.caption )
                elif typefile == 'audio':
                    await bale_bot.send_audio(bale_channel_id , bin_file , message.caption )
                else :
                    await bale_bot.send_document(bale_channel_id , bin_file , message.caption )
                
                await eitaa_bot.send_file(eitaa_channel_id , bin_file , message.caption)
                return "پیام ارسال شد"
            except Exception as e :
                return f"خطا در ارسال پیام \n\n{e}"
            

            
        else :
            if message.text :
                text = message.text
            elif message.caption:
                text = message.caption 
            try :
                await bale_bot.send_message(bale_channel_id , text )
                await eitaa_bot.send_message(eitaa_channel_id , text )
                return "پیام ارسال شد "
            except Exception as e :
                return f"خطا در ارسال پیام \n\n{e}"
            
            

async def send_leftover_hadith_bale():
    leftover_hadiths = db_hadith.return_bale_laftover()
    if not leftover_hadiths:
        return 'پیامی موجود نیست'

    try:
        with open(photo_url, 'rb') as photo:
            for hadith_text, hadith_id in leftover_hadiths:
                text = process_hadith_message(hadith_text, hadith_id)
                await bale_bot.send_photo(bale_channel_id, photo, text)
                db_hadith.mark_sent_bale(id=hadith_id)
        return "پیام‌ها در بله ارسال شدند"
    except Exception as e:
        return f'خطا در ارسال \n\n{e}'

    
async def send_leftover_hadith_eitaa():
    leftover_hadiths = db_hadith.return_eitaa_laftover()
    if not leftover_hadiths:
        return 'پیامی موجود نیست'

    try:
        with open(photo_url, 'rb') as photo:
            for hadith_text, hadith_id in leftover_hadiths:
                text = process_hadith_message(hadith_text, hadith_id)
                await eitaa_bot.send_file(bale_channel_id, photo, text)
                db_hadith.mark_sent_eitaa(id=hadith_id)
        return "پیام‌ها در ایتا ارسال شدند"
    except Exception as e:
        return f'خطا در ارسال \n\n{e}'



async def send_laftover_hadith():
    bale = await send_leftover_hadith_bale()
    eitaa =await send_leftover_hadith_eitaa()
    return f'ایتا \n {eitaa} \n\n بله \n {bale}'



async def send_leftover_note_eitaa():
    leftover_hadiths = db_notes.return_eitaa_laftover()
    if not leftover_hadiths:
        return 'پیامی موجود نیست'

    try:
        for hadith_text, hadith_id in leftover_hadiths:
            text = process_note_message(hadith_text, hadith_id)
            await eitaa_bot.send_message(bale_channel_id, text)
            db_notes.mark_sent_eitaa(id=hadith_id)
        return "پیام‌ها در ایتا ارسال شدند"
    except Exception as e:
        return f'خطا در ارسال \n\n{e}'

async def send_leftover_note_bale():
    leftover_hadiths = db_notes.return_bale_laftover()
    if not leftover_hadiths:
        return 'پیامی موجود نیست'

    try:
        for hadith_text, hadith_id in leftover_hadiths:
            text = process_note_message(hadith_text, hadith_id)
            await bale_bot.send_message(bale_channel_id, text)
            db_notes.mark_sent_bale(id=hadith_id)
        return "پیام‌ها در بله ارسال شدند"
    except Exception as e:
        return f'خطا در ارسال \n\n{e}'
    
    
async def send_laftover_note():
    bale = await send_leftover_note_bale()
    eitaa =await send_leftover_note_eitaa()
    return f'ایتا \n {eitaa} \n\n بله \n {bale}'



async def send_text_schaduler(text):
    try :
        bale = bale_bot.send_message(bale_channel_id , text)
        eitaa = eitaa_bot.send_message(eitaa_channel_id , text)
        await asyncio.gather(bale , eitaa )
    except Exception as e :
        return str(e)




async def send_tohid():
    text = '''
بِسْمِ اللَّهِ الرَّحْمَنِ الرَّحِیم
قُلْ هُوَ اللَّهُ أَحَدٌ ﴿١﴾

اللَّهُ الصَّمَدُ ﴿٢﴾

لَمْ یَلِدْ وَلَمْ یُولَدْ ﴿٣﴾

وَلَمْ یَکُنْ لَهُ کُفُوًا أَحَدٌ ﴿٤﴾ '''
    
    try :
        with open(tohid_audio_url ,'rb') as v :
            await bale_bot.send_audio(bale_channel_id , v , caption= f'{text} \n با خواندن سوره توحید و هدیه به حضرت صاحب الزمان (روحی و ارواح العالمين له الفدا) از او مدد بخواهیم') 
            await  eitaa_bot.send_file(eitaa_channel_id , v , caption= f'{text} \n با خواندن سوره توحید و هدیه به حضرت صاحب الزمان (روحی و ارواح العالمين له الفدا) از او مدد بخواهیم') 
            
            
            
    except Exception as e :
        return str(e)



async def send_salavat_8():
    text = '''اللّهُمَّ صَلِّ عَلَى عَلِیِّ بْنِ مُوسى الرِّضا
الْمُرْتَضَى الإِمامِ التَّقی النَّقی وَ حُجَّتِکَ
عَلَى مَنْ فَوْقَ الْأَرْضِ وَ مَنْ تَحْتَ الثَّرى
الصِّدِّیقِ الشَّهِیدِ صَلاةً کَثِیرَةً تَامَّةً زَاکِیَةً
مُتَوَاصِلَةً مُتَوَاتِرَةً مُتَرَادِفَةً کَأَفْضَلِ
مَا صَلَّیْتَ عَلَى أَحَدٍ مِنْ أَوْلِیائِکَ'''

    try :
        with open(salavat_audio_url ,'rb') as v :
            await eitaa_bot.send_file(eitaa_channel_id , v , caption=f'{text}') 
            await bale_bot.send_audio(bale_channel_id , v , caption= f'{text}')
            
    except Exception as e :
        return str(e)