FROM python:3.11-slim

# نصب وابستگی‌های سیستمی برای پکیج‌هایی مثل psycopg2
RUN apt-get update && apt-get install -y \
    gcc \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# کپی فایل‌های مورد نیاز
COPY requirements.txt .

# نصب pip و پکیج‌ها به صورت جداگانه برای دیباگ بهتر
RUN pip install --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt

# کپی کل پروژه
COPY . .

# تنظیم محیط برای خروجی لحظه‌ای
ENV PYTHONUNBUFFERED=1

# اجرای فایل اصلی
CMD ["python", "main.py"]
