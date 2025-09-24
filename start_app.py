import subprocess
import threading
import time
import webbrowser
import os
import sys
from pathlib import Path

def run_api():
    """Запуск API сервера"""
    print("🚀 Запуск API сервера на порту 8000...")
    try:
        # Переходим в папку api и запускаем main.py
        original_dir = os.getcwd()
        os.chdir("api")
        subprocess.call([sys.executable, "main.py"])
        os.chdir(original_dir)
    except Exception as e:
        print(f"❌ Ошибка запуска API: {e}")

def run_web_server():
    """Запуск простого веб-сервера для статики"""
    print("🌐 Запуск веб-сервера на порту 3000...")
    try:
        # Ждем немного, чтобы API успел запуститься
        time.sleep(3)
        original_dir = os.getcwd()
        
        # Проверяем существование папки web-app
        web_app_path = os.path.join(original_dir, "web-app")
        if not os.path.exists(web_app_path):
            print(f"❌ Папка {web_app_path} не найдена!")
            return
            
        os.chdir(web_app_path)
        print(f"📁 Запуск сервера в папке: {web_app_path}")
        subprocess.call([sys.executable, "-m", "http.server", "3000"])
        os.chdir(original_dir)
    except Exception as e:
        print(f"❌ Ошибка запуска веб-сервера: {e}")

def open_browser():
    """Открыть браузер через несколько секунд"""
    time.sleep(5)
    print("🌐 Открываем браузер...")
    # Сначала пробуем API сервер (он уже работает и раздает статику)
    webbrowser.open("http://localhost:8000")

def check_files():
    """Проверка наличия необходимых файлов"""
    required_files = [
        "api/main.py",
        "web-app/templates/index.html",
        ".env"
    ]
    
    missing_files = []
    for file in required_files:
        if not Path(file).exists():
            missing_files.append(file)
    
    if missing_files:
        print("❌ Отсутствуют файлы:")
        for file in missing_files:
            print(f"   - {file}")
        return False
    
    print("✅ Все необходимые файлы найдены")
    return True

def main():
    print("🎯 Quiz App - Запуск приложения")
    print("=" * 50)
    
    # Проверяем файлы
    if not check_files():
        print("\n❌ Не все файлы найдены. Создайте недостающие файлы.")
        input("Нажмите Enter для выхода...")
        return
    
    print("\n📦 Установка зависимостей...")
    try:
        subprocess.run([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"], 
                      check=True, capture_output=True)
        print("✅ Зависимости установлены")
    except subprocess.CalledProcessError as e:
        print(f"⚠️ Проблемы с установкой зависимостей: {e}")
        print("Продолжаем запуск...")
    
    print("\n🚀 Запуск серверов...")
    
    # Запускаем API в отдельном потоке
    api_thread = threading.Thread(target=run_api, daemon=True)
    api_thread.start()
    
    # Запускаем веб-сервер в отдельном потоке  
    web_thread = threading.Thread(target=run_web_server, daemon=True)
    web_thread.start()
    
    # Открываем браузер через несколько секунд
    browser_thread = threading.Thread(target=open_browser, daemon=True)
    browser_thread.start()
    
    print("\n✅ Серверы запущены!")
    print("📡 API сервер: http://localhost:8000")
    print("🌐 Веб приложение: http://localhost:3000")
    print("\n❌ Для остановки нажмите Ctrl+C")
    
    try:
        # Держим основной поток живым
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("\n\n👋 Завершение работы...")
        print("Серверы остановлены.")

if __name__ == "__main__":
    main()