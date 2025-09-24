@echo off
title Quiz App Launcher
color 0A

echo.
echo     ╔══════════════════════════════════════╗
echo     ║           QUIZ APP LAUNCHER          ║  
echo     ║                                      ║
echo     ║  🎯 Запуск приложения для тестов     ║
echo     ╚══════════════════════════════════════╝
echo.

echo 📦 Проверка зависимостей...
pip install -r requirements.txt >nul 2>&1
if errorlevel 1 (
    echo ⚠️ Ошибка при установке Python зависимостей
    echo Попробуйте запустить: pip install -r requirements.txt
    pause
    exit /b
)

echo ✅ Зависимости готовы
echo.
echo 🚀 Запуск Quiz App...
echo.

python start_app.py

echo.
echo 👋 Приложение завершено
pause