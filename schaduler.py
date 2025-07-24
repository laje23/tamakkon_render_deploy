import asyncio
from datetime import datetime
from utils import today
from send_message_handler import (
    send_text_schaduler,
    send_to_debuger,
    auto_send_hadith,
    send_tohid,
    auto_send_not,
    send_salavat_8,
)

async def scheduled_messages():
    while True:
        now = datetime.now()
        current_time = now.strftime("%H:%M")

        if current_time == "06:00":
            err = await send_text_schaduler(today())
            await send_to_debuger(f"[06:00] خطا در ارسال ذکر روز: {err}")

            tx = await auto_send_hadith()
            await send_to_debuger(f"[06:00] خطا در ارسال حدیث تصادفی: {tx}")

            err = await send_tohid()
            await send_to_debuger(f"[06:00] خطا در ارسال یادآور سوره توحید: {err}")

        elif current_time == "08:00":
            tx = await auto_send_not()
            await send_to_debuger(f"[08:00] خطا در ارسال یادداشت استاد: {tx}")

            err = await send_salavat_8()
            await send_to_debuger(f"[08:00] خطا در ارسال صلوات خاصه امام رضا: {err}")

        elif current_time == "12:00":
            tx = await auto_send_hadith()
            await send_to_debuger(f"[12:00] خطا در ارسال حدیث تصادفی: {tx}")

            err = await send_tohid()
            await send_to_debuger(f"[12:00] خطا در ارسال یادآور سوره توحید: {err}")

        elif current_time == "16:00":
            tx = await auto_send_not()
            await send_to_debuger(f"[16:00] خطا در ارسال یادداشت استاد: {tx}")

            err = await send_tohid()
            await send_to_debuger(f"[16:00] خطا در ارسال یادآور سوره توحید: {err}")
            
        elif current_time == '18:34':
            print('.....')

        elif current_time == "20:00":
            err = await send_salavat_8()
            await send_to_debuger(f"[20:00] خطا در ارسال صلوات خاصه امام رضا: {err}")

            tx = await auto_send_hadith()
            await send_to_debuger(f"[20:00] خطا در ارسال حدیث تصادفی: {tx}")

            err = await send_tohid()
            await send_to_debuger(f"[20:00] خطا در ارسال یادآور سوره توحید: {err}")

        elif current_time == "22:00":
            tx = await auto_send_not()
            await send_to_debuger(f"[22:00] خطا در ارسال یادداشت استاد: {tx}")

            err = await send_tohid()
            await send_to_debuger(f"[22:00] خطا در ارسال یادآور سوره توحید: {err}")
        await asyncio.sleep(60)  # هر دقیقه چک می‌کنیم
