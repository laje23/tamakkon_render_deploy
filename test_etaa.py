import httpx
from balethon import Client
from balethon.client import messages

app = Client(token="87843638:AVJFrqDghxrU5mepoeZ5i49U8kwIOr75jLinpo7q")  # فقط برای پاسخ دادن در بله

async def send_message_to_eita(text: str):
    url = f"{BASE_URL}/sendMessage"
    data = {
        "chat_id": CHAT_ID,
        "text": text
    }
    async with httpx.AsyncClient() as client:
        resp = await client.post(url, json=data)
        return resp.json()

@app.on_message()
async def handler(client: Client, message: messages):
    await message.reply("در حال ارسال پیام به ایتا...")
    result = await send_message_to_eita("📢 پیام تست از ربات من به کانال ایتا")

    if result.get("ok"):
        await message.reply("✅ پیام با موفقیت به کانال ارسال شد.")
    else:
        await message.reply(f"❌ خطا در ارسال: {result}")


app.run()