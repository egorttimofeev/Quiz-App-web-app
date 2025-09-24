# Этот файл перемещен в api/main.py
# Для запуска используйте:
# python start_app.py

import os
import sys

print("⚠️  Используйте 'python start_app.py' для запуска приложения")
print("📁 Основной код находится в папке api/")

# Перенаправляем на правильный запуск
if __name__ == "__main__":
    try:
        exec(open('start_app.py').read())
    except FileNotFoundError:
        print("❌ Файл start_app.py не найден")
        print("Создайте его с помощью команды в README.md")