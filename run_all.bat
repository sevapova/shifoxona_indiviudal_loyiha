@echo off
echo ===================================================
echo   🏥 SHIFOXONA TIZIMI: SERVER VA BOTNI ISHGA TUSHIRISH
echo ===================================================

:: 1. Django Serverini yangi oynada ochish
echo 🚀 Django serveri ishga tushmoqda...
start cmd /k "venv\Scripts\activate && python manage.py runserver"

:: 2. Telegram Botni yangi oynada ochish
echo 🤖 Telegram bot ishga tushmoqda...
start cmd /k "venv\Scripts\activate && python bot.py"

echo ===================================================
echo ✅ Ikkala tizim ham alohida oynalarda ochildi.
echo 🌐 Sayt: http://127.0.0.1:8000/
echo ===================================================
pause
