import httpx




class EitaaBot:
    
    def __init__(self , eitaa_bot_token ):
        self.bot_token_eitaa = eitaa_bot_token
        self.eitaa_base_url = f'https://eitaayar.ir/api/{eitaa_bot_token}'

    async def send_message(self ,chat_id: int, text: str):
        url = f"{self.eitaa_base_url}/sendMessage"
        payload = {
            "chat_id": chat_id,
            "text": text
        }
        async with httpx.AsyncClient() as client:
            res = await client.post(url, json=payload)
            dic = res.json()
            if dic['ok'] == 'true':
                return True
            return False
        
        
    async def send_file(self ,chat_id: int, file_url: str, caption=""):
        url = f"{self.eitaa_base_url}/sendFile"
        payload = {
            "chat_id": chat_id,
            "caption": caption,
        }
        async with httpx.AsyncClient() as client:
            res = await client.post(url, data=payload, files={"file": file_url})
            dic = res.json()
            if dic['ok'] == 'true':
                return True
            return dic 
