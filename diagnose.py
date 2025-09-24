import subprocess
import sys
import os
from pathlib import Path

def check_python():
    print(f"🐍 Python: {sys.version}")
    return True

def check_node():
    try:
        result = subprocess.run(['node', '--version'], capture_output=True, text=True)
        if result.returncode == 0:
            print(f"📦 Node.js: {result.stdout.strip()}")
            return True
    except:
        pass
    print("❌ Node.js не установлен")
    return False

def check_postgresql():
    try:
        result = subprocess.run(['pg_config', '--version'], capture_output=True, text=True)
        if result.returncode == 0:
            print(f"🐘 PostgreSQL: {result.stdout.strip()}")
            return True
    except:
        pass
    print("❌ PostgreSQL не найден в PATH (но может быть установлен)")
    return False

def check_env_file():
    env_path = Path('.env')
    if env_path.exists():
        print("✅ Файл .env найден")
        
        # Проверяем содержимое .env
        try:
            with open('.env', 'r', encoding='utf-8') as f:
                content = f.read()
                
            if 'your_password' in content:
                print("⚠️ Нужно заменить 'your_password' на реальный пароль PostgreSQL")
                return False
            if 'your_telegram_bot_token' in content:
                print("⚠️ Нужно заменить 'your_telegram_bot_token' на реальный токен бота")
                return False
            if 'your_admin_telegram_id' in content:
                print("⚠️ Нужно заменить 'your_admin_telegram_id' на ваш Telegram ID")
                return False
                
            print("✅ Файл .env настроен")
            return True
        except Exception as e:
            print(f"⚠️ Ошибка чтения .env: {e}")
            return False
    else:
        print("❌ Файл .env не найден")
        return False

def check_required_files():
    required_files = [
        "api/main.py",
        "api/app.py", 
        "web-app/templates/index.html",
        "requirements.txt",
        "start_app.py"
    ]
    
    all_found = True
    for file in required_files:
        if Path(file).exists():
            print(f"✅ {file}")
        else:
            print(f"❌ {file}")
            all_found = False
    
    return all_found

def check_python_packages():
    required_packages = [
        'fastapi',
        'uvicorn', 
        'psycopg2',
        'python-dotenv',
        'pydantic'
    ]
    
    missing_packages = []
    
    for package in required_packages:
        try:
            __import__(package.replace('-', '_'))
            print(f"✅ {package}")
        except ImportError:
            print(f"❌ {package}")
            missing_packages.append(package)
    
    return len(missing_packages) == 0

def main():
    print("🔍 Диагностика системы Quiz App")
    print("=" * 50)
    
    print("\n📋 Системные требования:")
    python_ok = check_python()
    node_ok = check_node()
    postgres_ok = check_postgresql()
    
    print("\n📁 Файлы проекта:")
    files_ok = check_required_files()
    
    print("\n⚙️ Конфигурация:")
    env_ok = check_env_file()
    
    print("\n📦 Python пакеты:")
    packages_ok = check_python_packages()
    
    print("\n" + "=" * 50)
    
    all_good = python_ok and files_ok and env_ok and packages_ok
    
    if all_good:
        print("✅ Все компоненты готовы!")
        print("\n🚀 Можете запускать приложение:")
        print("   python start_app.py")
        print("   ИЛИ")  
        print("   start.bat")
    else:
        print("❌ Нужно исправить ошибки выше")
        
        if not packages_ok:
            print("\n📦 Для установки Python пакетов выполните:")
            print("   pip install -r requirements.txt")
        
        if not env_ok:
            print("\n⚙️ Для настройки .env файла:")
            print("   1. Установите PostgreSQL")
            print("   2. Создайте Telegram бота через @BotFather")
            print("   3. Узнайте свой Telegram ID через @userinfobot")
            print("   4. Отредактируйте .env файл")
        
        if not files_ok:
            print("\n📁 Некоторые файлы отсутствуют. Проверьте структуру проекта.")

if __name__ == "__main__":
    main()