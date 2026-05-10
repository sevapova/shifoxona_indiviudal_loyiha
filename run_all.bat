@echo off
echo Shifoxona tizimi ishga tushmoqda...
start cmd /k "venv\Scripts\activate && python manage.py runserver"
timeout /t 5
start cmd /k "venv\Scripts\activate && python bot.py"
echo Barcha tizimlar ishga tushirildi.
pause
