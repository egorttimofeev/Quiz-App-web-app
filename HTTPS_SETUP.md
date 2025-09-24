# 🔐 Настройка HTTPS для Telegram Web App

## Проблема
Telegram Web App требует HTTPS соединение. Локальный HTTP сервер (http://localhost:8000) не будет работать в Telegram.

## ✅ Решение 1: ngrok (Рекомендуется для разработки)

### 1. Установка ngrok
1. Перейдите на https://ngrok.com/download
2. Скачайте ngrok для Windows
3. Распакуйте в папку (например: `C:\ngrok\`)
4. Добавьте в PATH или используйте полный путь

### 2. Регистрация (опционально)
```bash
# Зарегистрируйтесь на ngrok.com и получите authtoken
ngrok authtoken your_auth_token_here
```

### 3. Запуск
**Вариант А - Автоматический:**
```bash
# Запустите готовый скрипт
.\run_https.bat
```

**Вариант Б - Ручной:**
```bash
# Терминал 1: Запустите API сервер
.\run_server.bat

# Терминал 2: Запустите ngrok туннель
ngrok http 8000
```

### 4. Настройка бота
1. Скопируйте HTTPS URL из ngrok (например: `https://abc123.ngrok.io`)
2. В @BotFather используйте:
   ```
   /setmenubutton
   [выберите бота]
   Текст: 🎯 Начать квиз
   URL: https://abc123.ngrok.io/app
   ```

## ✅ Решение 2: Cloudflare Tunnel (Бесплатно)

### 1. Установка
```bash
# Скачайте cloudflared
# https://developers.cloudflare.com/cloudflare-one/connections/connect-apps/install-and-setup/
```

### 2. Запуск туннеля
```bash
cloudflared tunnel --url http://localhost:8000
```

### 3. Получите публичный URL и используйте в @BotFather

## ✅ Решение 3: localtunnel

### 1. Установка
```bash
npm install -g localtunnel
```

### 2. Запуск
```bash
# Терминал 1: API сервер
.\run_server.bat

# Терминал 2: Туннель
lt --port 8000 --subdomain quiz-app-your-name
```

### 3. URL будет: `https://quiz-app-your-name.loca.lt`

## 🌐 Решение 4: Деплой на хостинг (Продакшн)

### Railway (Рекомендуется)
1. Создайте аккаунт на railway.app
2. Подключите GitHub репозиторий
3. Railway автоматически развернет приложение
4. Получите домен: `https://your-app.railway.app`

### Heroku
```bash
# Создайте Procfile
echo "web: uvicorn api.app:app --host 0.0.0.0 --port $PORT" > Procfile

# Деплой
heroku create your-quiz-app
git add .
git commit -m "Deploy"
git push heroku main
```

### Render
1. Подключите GitHub на render.com
2. Выберите "Web Service"
3. Build Command: `pip install -r requirements-minimal.txt`
4. Start Command: `uvicorn api.app:app --host 0.0.0.0 --port $PORT`

## 🔧 Troubleshooting

### ngrok показывает ошибку "tunnel not found"
```bash
# Переустановите ngrok или используйте другой порт
ngrok http 8001
```

### "Failed to complete tunnel connection"
```bash
# Проверьте что API сервер запущен
curl http://localhost:8000/health
```

### Telegram показывает "Unable to load page"
1. Убедитесь что используете HTTPS URL
2. Проверьте что туннель активен
3. Попробуйте обновить URL в @BotFather

### CORS ошибки
Убедитесь что в `api/app.py` настроен CORS:
```python
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # В продакшене указать конкретные домены
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```

## 📱 Тестирование

1. **Локально:** http://localhost:8000/app
2. **HTTPS туннель:** https://xxx.ngrok.io/app  
3. **В Telegram:** Нажмите кнопку меню бота

## 🚀 Быстрый чек-лист

- [ ] API сервер запущен (`.\run_server.bat`)
- [ ] ngrok установлен и запущен (`ngrok http 8000`)
- [ ] HTTPS URL скопирован из ngrok
- [ ] URL обновлен в @BotFather через `/setmenubutton`
- [ ] Тест в браузере: `https://xxx.ngrok.io/app`
- [ ] Тест в Telegram: кнопка меню бота

---
*Для продакшена используйте постоянный хостинг вместо ngrok*