from models import lecture, clips, hadith, notes, books

if __name__ == "__main__":
    lecture.create_table()
    clips.create_table()
    notes.create_table()
    hadith.create_table()
    books.create_table()
