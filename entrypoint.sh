#!/bin/bash

echo "✅ اجرای فایل اولیه (مثلاً ایجاد جداول)..."
python init_script.py

echo "🚀 اجرای برنامه اصلی..."
python main.py
