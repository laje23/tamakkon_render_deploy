from config import bot , back_menu , db_notes , group_mirror_id , process_note_message





async def first_step(message):
    if not message.text.isdigit() or int(message.text) <= 0:
        await bot.send_message(message.chat.id, "❗️ لطفاً فقط عدد مثبت وارد کنید.", back_menu())
        return

    message.author.set_data("note_id", int(message.text))  # 👈 ذخیره برای مرحله بعد
    await bot.send_message(message.chat.id, "متن یادداشت رو وارد کنید", back_menu())
    message.author.set_state('INPUT_TEXT_NOTE')  # 👈 رفتن به مرحله بعد
    
    
    
async def next_step(message):
    note_id = message.author.data.get("note_id")  # 👈 خواندن شماره ذخیره‌شده

    try:
        sent = await bot.send_message(group_mirror_id, process_note_message(message.text, note_id))
        db_notes.save_note(note_id, sent.id)
        message.author.del_state()
        await bot.send_message(message.chat.id, '✅ یادداشت با موفقیت ذخیره شد.', back_menu())
    except Exception as e:
        await bot.send_message(message.chat.id, f"⚠️ خطا:\n{e}", back_menu())