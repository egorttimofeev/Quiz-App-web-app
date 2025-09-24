# Инструкции по развертыванию Quiz App

## 📋 Пошаговая инструкция установки

### 1. Подготовка системы

#### Windows:
```cmd
# Проверьте установку Python
python --version
# Должен быть Python 3.8+

# Проверьте установку Node.js
node --version
npm --version
# Должен быть Node.js 16+
```

#### Если Python не установлен:
1. Скачайте с https://python.org
2. При установке обязательно отметьте "Add to PATH"

#### Если Node.js не установлен:
1. Скачайте с https://nodejs.org (LTS версия)
2. Установите с настройками по умолчанию

### 2. Установка PostgreSQL

#### Windows:
1. Скачайте с https://www.postgresql.org/download/windows/
2. При установке:
   - Запомните пароль для пользователя `postgres`
   - Порт оставьте 5432
   - Кодировка UTF-8
3. После установки создайте базу данных:
   ```sql
   CREATE DATABASE quiz_app;
   ```

#### Или используйте Docker:
```bash
docker run --name quiz-postgres -e POSTGRES_PASSWORD=mypassword -e POSTGRES_DB=quiz_app -p 5432:5432 -d postgres:13
```

### 3. Настройка проекта

1. **Клонируйте репозиторий:**
   ```bash
   git clone <your-repo-url>
   cd web-app
   ```

2. **Настройте .env файл:**
   ```env
   DATABASE_URL="postgresql://postgres:YOUR_PASSWORD@localhost:5432/quiz_app"
   TELEGRAM_BOT_TOKEN="YOUR_BOT_TOKEN"
   TELEGRAM_ADMIN_ID="YOUR_TELEGRAM_USER_ID"
   SECRET_KEY="some-random-secret-key"
   DEBUG=True
   API_PORT=8000
   WEB_PORT=3000
   ```

### 4. Создание Telegram бота

1. **Напишите @BotFather в Telegram:**
   ```
   /newbot
   Название: Quiz App Bot
   Username: yourquizapp_bot
   ```

2. **Получите токен и добавьте в .env**

3. **Настройте Web App:**
   ```
   /setmenubutton
   Выберите бота
   Введите название кнопки: Открыть Quiz
   Введите URL: https://yourdomain.com (или для разработки: https://abc123.ngrok.io)
   ```

### 5. Запуск приложения

#### Автоматически (рекомендуется):
```bash
# Windows
start.bat

# Linux/macOS
chmod +x start.sh
./start.sh
```

#### Вручную:
```bash
# 1. Установите зависимости
pip install -r requirements.txt
npm install

# 2. Установите PM2 глобально
npm install -g pm2

# 3. Настройте Prisma
npx prisma generate
npx prisma migrate deploy

# 4. Заполните базу данных
python seed_database.py

# 5. Запустите приложение
npm run dev
```

### 6. Проверка работы

1. **API доступно:** http://localhost:8000
2. **Web App:** http://localhost:8000
3. **API документация:** http://localhost:8000/docs
4. **База данных:** `npx prisma studio` (http://localhost:5555)

## 🔧 Управление приложением

### PM2 команды:
```bash
npm run dev      # Запуск в режиме разработки
npm run prod     # Запуск в production
npm run stop     # Остановка всех процессов
npm run restart  # Перезапуск
npm run logs     # Просмотр логов
```

### Управление вопросами:
```bash
python manage.py  # Интерактивное меню управления
```

## 🌐 Развертывание в production

### 1. Подготовка сервера

```bash
# Ubuntu/Debian
sudo apt update
sudo apt install python3 python3-pip nodejs npm postgresql postgresql-contrib nginx

# CentOS/RHEL
sudo yum install python3 python3-pip nodejs npm postgresql postgresql-server nginx
```

### 2. Настройка Nginx (опционально)

```nginx
server {
    listen 80;
    server_name yourdomain.com;

    location / {
        proxy_pass http://localhost:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
}
```

### 3. SSL сертификат

```bash
# Certbot для Let's Encrypt
sudo apt install certbot python3-certbot-nginx
sudo certbot --nginx -d yourdomain.com
```

### 4. Production настройки

В `.env`:
```env
DEBUG=False
DATABASE_URL="postgresql://quiz_user:secure_password@localhost:5432/quiz_app"
```

Запуск:
```bash
npm run prod
```

## 🔍 Отладка проблем

### Частые ошибки:

1. **"Module not found" ошибки:**
   ```bash
   pip install -r requirements.txt
   npm install
   ```

2. **Ошибка подключения к БД:**
   - Проверьте, что PostgreSQL запущен
   - Проверьте DATABASE_URL в .env
   - Проверьте пароль и имя базы

3. **Ошибка импорта Prisma:**
   ```bash
   npx prisma generate
   ```

4. **PM2 не найден:**
   ```bash
   npm install -g pm2
   ```

5. **Порт уже используется:**
   ```bash
   # Найти процесс на порту 8000
   netstat -ano | findstr :8000
   # Завершить процесс
   taskkill /PID <PID> /F
   ```

### Просмотр логов:

```bash
# Логи приложения
npm run logs

# Конкретный процесс
pm2 logs quiz-api

# Логи в файлах
tail -f logs/api-combined.log
```

## 📱 Интеграция с Telegram

### Webhook настройка:

```bash
# Установите webhook (замените URL и токен)
curl -X POST "https://api.telegram.org/botYOUR_BOT_TOKEN/setWebhook" \
     -H "Content-Type: application/json" \
     -d '{"url": "https://yourdomain.com/api/telegram/webhook"}'
```

### Тестирование Web App:

1. Откройте бота в Telegram
2. Нажмите кнопку меню или отправьте команду
3. Должен открыться веб-интерфейс

## 🔐 Безопасность

### Рекомендации для production:

1. **Используйте сильные пароли для БД**
2. **Измените SECRET_KEY на случайную строку**
3. **Настройте файрвол:**
   ```bash
   sudo ufw allow 22
   sudo ufw allow 80
   sudo ufw allow 443
   sudo ufw enable
   ```
4. **Регулярно обновляйте зависимости**
5. **Настройте резервное копирование БД**

### Резервное копирование:

```bash
# Создание бэкапа
pg_dump quiz_app > backup_$(date +%Y%m%d_%H%M%S).sql

# Восстановление
psql quiz_app < backup_file.sql
```

## 🎯 Мониторинг

### PM2 Monitoring:

```bash
# Веб-интерфейс мониторинга
pm2 web

# Консольный мониторинг
pm2 monit
```

### Системные ресурсы:

```bash
# Использование диска
df -h

# Использование памяти
free -h

# Процессы
htop
```

## 📞 Поддержка

Если возникают проблемы:

1. Проверьте логи: `npm run logs`
2. Убедитесь, что все сервисы запущены
3. Проверьте конфигурацию в `.env`
4. Проверьте статус PM2: `pm2 status`

Для получения помощи создайте issue с описанием проблемы и логами.