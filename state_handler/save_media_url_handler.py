import mimetypes
from models.media import save_media  # همان تابع save_media که در نسخه sync نوشتیم

async def first_step_save_media(message):
    
    file_id = None
    type_file = None
    if message.photo:
        photo = message.photo[-1]
        file_id = photo.id
        type_file = "photo"
    elif message.audio:
        file_id = message.audio.id
        type_file = "audio"
    elif message.video:
        file_id = message.video.id
        type_file = "video"

    if file_id is None:
        return False
    # تشخیص نوع فایل از روی نام فایل
    media_type, _ = mimetypes.guess_type(filename)

    # ذخیره در دیتابیس
    media_db_id = save_media(file_id, filename, url)  # تابع sync قبلی هم می‌تواند همینطور کار کند

    if media_db_id:
        return f"✅ فایل '{filename}' با موفقیت ذخیره شد (نوع: {media_type})."
    else:
        return f"ℹ️ فایل '{filename}' قبلاً ذخیره شده است."
