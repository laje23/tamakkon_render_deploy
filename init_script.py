from models import lecture, clips, hadith, notes, books , media
from config import eitaa_bot, eitaa_channel_id_test
import asyncio

if __name__ == "__main__":
    lecture.create_table()
    clips.create_table()
    notes.create_table()
    notes.create_table_parts()
    hadith.create_table()
    books.create_table()
    media.create_table()
    asyncio.run(eitaa_bot.send_message(eitaa_channel_id_test, "بات ری استارت شد"))
