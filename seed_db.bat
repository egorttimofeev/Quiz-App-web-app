@echo off
cd /d "d:\github\web-app"
echo 🌱 Заполнение базы данных...
"C:\Users\nasus\AppData\Local\Microsoft\WindowsApps\python.exe" seed_database.py
echo.
echo ✅ Готово! База данных заполнена.
pause