import os
import subprocess
import datetime


def backup_database():
    """
    بکاپ کامل دیتابیس با pg_dump می‌گیره و داخل فولدر جاری ذخیره می‌کنه
    """
    db_name = os.getenv("PGDATABASE")
    db_user = os.getenv("POSTGRES")
    db_host = os.getenv("PGHOST")
    backup_file = f"backup_{db_name}_{datetime.datetime.now():%Y%m%d_%H%M%S}.sql"

    cmd = [
        "pg_dump",
        "-U", db_user,
        "-h", db_host,
        "-F", "c",  
        "-f", backup_file,
        db_name
    ]

    try:
        # پسورد از env گرفته میشه
        env = os.environ.copy()
        env["PGPASSWORD"] = os.getenv("PGPASSWORD")

        subprocess.run(cmd, check=True, env=env)
        return {'ok' : True , 'file_path ': backup_file , 'err' : ''}
    except subprocess.CalledProcessError as e:
        return {'ok' : False , 'file_path ': '' , 'err' : e}
