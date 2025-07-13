import os
import httpx

# گرفتن مقادیر از فایل .env
bot_token_eitaa = os.getenv("EITAA_BOT_TOKEN")
eitaa_base_url = os.getenv("BASE_EITAA_URL")


# ارسال پیام متنی به گروه یا کانال
async def send_text_to_group(chat_id: int, text: str):
    '''chat_id =-= mirror_eitaa '''
    url = f"{eitaa_base_url}/sendMessage"
    payload = {
        "bot_token": bot_token_eitaa,
        "chat_id": chat_id,
        "text": text
    }
    async with httpx.AsyncClient() as client:
        res = await client.post(url, json=payload)
        return res.json()
    
    
# ارسال فایل (تصویر، صوت، PDF...) به گروه یا کانال
async def send_file_to_group(chat_id: int, file_path: str, caption=""):
    url = f"{eitaa_base_url}/sendFile"
    payload = {
        "bot_token": bot_token_eitaa,
        "chat_id": str(chat_id),
        "caption": caption
    }
    async with httpx.AsyncClient() as client:
        with open(file_path, "rb") as f:
            res = await client.post(url, data=payload, files={"file": f})
        return res.json()



# کپی کردن پیام با آیدی از یک چت به چت دیگر (بدون فوروارد)
async def copy_message_by_id(source_chat_id: int, message_id: int, target_chat_id: int):
    url = f"{eitaa_base_url}/copyMessage"
    payload = {
        "bot_token": bot_token_eitaa,
        "from_chat_id": source_chat_id,
        "message_id": message_id,
        "chat_id": target_chat_id
    }
    async with httpx.AsyncClient() as client:
        res = await client.post(url, json=payload)
        return res.json()

