from config import *




async def send_hadith_to_bale():
    try:
        hadith_id = db_hadith.select_random_hadith()
        if hadith_id:
            await bot.copy_message(chanel_bale_id, group_mirror_id, hadith_id)
            db_hadith.sent_message(hadith_id)
            return "✅ حدیث ارسال شد."
        else :
            return "📚 همه احادیث ارسال شده‌اند."
    except Exception as e:
        return f"⛔️ خطا در ارسال حدیث:\n{e}"


