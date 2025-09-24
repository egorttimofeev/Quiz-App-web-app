import uvicorn
import os
from dotenv import load_dotenv

# Загружаем переменные окружения из родительской папки
load_dotenv("../.env")

# Импортируем приложение
from app import app

if __name__ == "__main__":
    port = int(os.getenv("API_PORT", 8000))
    print(f"🚀 Запуск API сервера на порту {port}...")
    uvicorn.run(
        "app:app",
        host="0.0.0.0", 
        port=port,
        reload=True,
        log_level="info"
    )