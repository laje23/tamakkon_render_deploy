import httpx

TOKEN = '803ca9a53ea80522be5fcb773f73a59953f395581b22e407a721f598a5513c4e'
URL = 'https://core.gap.im/v1/messages'

headers = {
    'Authorization': f'Bearer {TOKEN}',
    'Content-Type': 'application/json'
}

payload = {
    "chat_id": "+989106479724",
    "type": "text",
    "data": "سلام! این یک پیام تست است."
}

try:
    with httpx.Client() as client:
        response = client.post(URL, json=payload, headers=headers)
        response.raise_for_status()  # اگر خطا بود Exception می‌زنه
        print("پیام با موفقیت ارسال شد:")
        print(response.json())
except httpx.HTTPStatusError as e:
    print(f"خطای HTTP دریافت شد: {e.response.status_code}")
    print(e.response.text)
except Exception as e:
    print("خطای دیگری رخ داد:")
    print(e)
