import httpx

class GapBot:
    def __init__(self, token):
        self.token = token
        self.api_url = f"https://api.gap.im/bot{token}"

    async def send_message(self, chat_id, text):
        url = f"{self.api_url}/sendMessage"
        payload = {
            "chat_id": chat_id,
            "text": text
        }
        async with httpx.AsyncClient() as client:
            response = await client.post(url, json=payload)
            return response.json().get("ok", False)

    async def send_file(self, chat_id, file_path, caption=""):
        url = f"{self.api_url}/sendDocument"
        payload = {
            "chat_id": chat_id,
            "caption": caption
        }
        async with httpx.AsyncClient() as client:
            with open(file_path, "rb") as f:
                files = {"document": f}
                response = await client.post(url, data=payload, files=files)
            return response.json().get("ok", False)
