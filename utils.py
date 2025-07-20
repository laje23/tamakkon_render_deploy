import io

async def get_photo_bytes(message, bot) -> bytes | None:
    if message.photo:
        photo = message.photo[-1]  # بزرگترین عکس
        file_id = photo.id  # گرفتن شناسه فایل

        content = await bot.download(file_id)  # دانلود محتوا

        bio = io.BytesIO(content)
        bio.seek(0)
        return bio.read()
    return None

