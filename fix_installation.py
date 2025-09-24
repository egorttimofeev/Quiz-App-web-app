import subprocess
import sys
import os

def run_command(command):
    """Выполнить команду и показать результат"""
    print(f"🔄 Выполняю: {command}")
    try:
        result = subprocess.run(command, shell=True, capture_output=True, text=True, encoding='utf-8')
        if result.returncode == 0:
            print(f"✅ Успешно")
            if result.stdout:
                print(result.stdout)
        else:
            print(f"❌ Ошибка:")
            print(result.stderr)
            return False
    except Exception as e:
        print(f"❌ Исключение: {e}")
        return False
    return True

def main():
    print("🚀 Исправление проблем с установкой Python 3.13")
    print("=" * 50)
    
    # 1. Обновляем pip
    print("\n1. Обновление pip...")
    run_command("python -m pip install --upgrade pip")
    
    # 2. Устанавливаем wheel
    print("\n2. Установка wheel...")
    run_command("pip install wheel setuptools")
    
    # 3. Пробуем установить паке