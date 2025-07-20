from config import db_hadith , bale_bot , back_menu , bale_channel_id , bale_group_mirror_id , answer_y_n



async def handel_number_hadith(message):
    if not message.text.isdigit() or  int(message.text)<= 0:
        await bale_bot.send_message(message.chat.id, "❗️ لطفاً فقط عدد مثبت وارد کنید.")
        return

    try:
        result = db_hadith.select_hadith_by_id(int(message.text))
        if not result:
            await bale_bot.send_message(message.chat.id, "❌ حدیث یافت نشد." , back_menu())
            return

        msg_id, sent = result
        if sent == 1:
            await message.reply("این حدیث قبلاً ارسال شده است ❗. اگر مایل به ارسال دوباره آن هستید روی شناسه آن کلیک کنید", answer_y_n(msg_id))
            return

        await bale_bot.copy_message(bale_channel_id, bale_group_mirror_id, msg_id)
        db_hadith.sent_message(msg_id)
        await bale_bot.send_message(message.chat.id, "✅ حدیث ارسال شد." , back_menu())
        message.author.del_state()
    except Exception as e:
        await bale_bot.send_message(message.chat.id, f"⚠️ خطا:\n{e}" , back_menu())