@echo off
echo 🚀 Запуск Quiz App с HTTPS через ngrok
echo.
echo 📋 Убедитесь что ngrok установлен: https://ngrok.com/download
echo.

REM Запускаем API сервер в фоне
echo 🌐 Запуск API сервера...
start "Quiz API" cmd /k "cd /d d:\github\web-app && "C:\Users\nasus\AppData\Local\Microsoft\WindowsApps\python.exe" api\app.py"

REM Ждем немного чтобы сервер запустился
timeout /t 3 /nobreak >nul

REM Запускаем ngrok туннель
echo 🔗 Создание HTTPS туннеля через ngrok...
echo.
echo ⚠️  ВАЖНО: Скопируйте https:// URL из ngrok и используйте его в @BotFather!
echo.

REM Проверяем установлен ли ngrok
where ngrok >nul 2>nul
if %errorlevel% neq 0 (
    echo ❌ ngrok не найден!
    echo 💡 Скачайте и установите: https://ngrok.com/download
    echo 📝 После установки добавьте ngrok в PATH
    pause
    exit /b 1
)

REM Запускаем ngrok
ngrok http 8000

echo.
echo 🛑 ngrok остановлен
pause