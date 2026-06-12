# Quiz App - Telegram Web App

Веб-приложение для проведения тестов с интеграцией в Telegram, построенное на современном стеке технологий.

## 🛠 Технологический стек

- **Backend**: Python + FastAPI
- **Frontend**: HTML5 + CSS3 + JavaScript
- **Database**: PostgreSQL
- **ORM**: Prisma
- **Process Manager**: PM2
- **Integration**: Telegram Web App API

## 📋 Функциональность

### Основные возможности:
- ✅ Приветственный экран с информацией о тесте
- ✅ Переключение темы (светлая/темная)
- ✅ Тест из 10 вопросов с 4 вариантами ответов
- ✅ Таймер и счетчик вопросов
- ✅ Навигация между вопросами (кнопка "Назад")
- ✅ Результаты с детализацией неправильных ответов
- ✅ Таблица лидеров с результатами всех пользователей
- ✅ Система оплаты пересдач (200 Telegram Stars)
- ✅ Случайная выборка вопросов из базы (50+ вопросов)
- ✅ Ссылка на админа для предложений
- ✅ Автоматическое сохранение пользователей из Telegram

### Правила тестирования:
- 10 вопросов в тесте
- 4 варианта ответа на каждый вопрос
- 1 правильный ответ
- Для прохождения нужно 7+ правильных ответов
- Первое прохождение бесплатно
- Пересдачи за 200 Telegram Stars

## 🚀 Установка и запуск

### Предварительные требования

1. **Python 3.8+**
   ```bash
   python --version
   ```

2. **Node.js 16+**
   ```bash
   node --version
   npm --version
   ```

3. **PostgreSQL 12+**
   - Скачать с [официального сайта](https://www.postgresql.org/download/)
   - Создать базу данных `quiz_app`
   - Запомнить пароль пользователя `postgres`

4. **PM2 (глобально)**
   ```bash
   npm install -g pm2
   ```

### Быстрый старт

1. **Клонирование репозитория**
   ```bash
   git clone <repository-url>
   cd web-app
   ```

2. **Настройка переменных окружения**
   Отредактируйте файл `.env`:
   ```env
   DATABASE_URL="postgresql://postgres:your_password@localhost:5432/quiz_app"
   TELEGRAM_BOT_TOKEN="your_telegram_bot_token"
   TELEGRAM_ADMIN_ID="your_admin_telegram_id"
   SECRET_KEY="your_secret_key_here"
   DEBUG=True
   TELEGRAM_STARS_PROVIDER_TOKEN="your_provider_token"
   API_PORT=8000
   WEB_PORT=3000
   ```

3. **Автоматический запуск (Windows)**
   ```bash
   start.bat
   ```

   **Или для Linux/macOS**
   ```bash
   chmod +x start.sh
   ./start.sh
   ```

4. **Или ручная установка**
   ```bash
   # Установка Python зависимостей
   pip install -r requirements.txt

   # Установка Node.js зависимостей
   npm install

   # Генерация Prisma клиента
   npx prisma generate

   # Применение миграций
   npx prisma migrate deploy

   # Заполнение базы данных
   python seed_database.py

   # Запуск приложения
   npm run dev
   ```

## 🔧 Настройка Telegram Bot

### Создание бота

1. Напишите [@BotFather](https://t.me/BotFather) в Telegram
2. Создайте нового бота: `/newbot`
3. Получите токен и добавьте в `.env`

### Настройка Web App

1. В [@BotFather] выберите вашего бота
2. Используйте `/setmenubutton`
3. Укажите URL: `https://yourdomain.com` (или ngrok для разработки)

### Настройка платежей

1. В [@BotFather]: `/mybots` → ваш бот → `Payments`
2. Выберите провайдера или используйте Telegram Stars
3. Получите provider token и добавьте в `.env`

## 📱 Структура проекта

```
web-app/
├── api/                    # Backend API
│   ├── main.py            # Главный файл FastAPI
│   ├── models/            # Модели данных
│   │   └── schemas.py
│   ├── routes/            # API маршруты
│   │   ├── users.py
│   │   ├── questions.py
│   │   ├── tests.py
│   │   └── telegram.py
│   └── services/          # Сервисы
│       └── database.py
├── web-app/               # Frontend
│   ├── templates/         # HTML шаблоны
│   │   └── index.html
│   └── static/           # Статические файлы
│       ├── css/
│       │   └── style.css
│       └── js/
│           └── app.js
├── prisma/               # Схема базы данных
│   └── schema.prisma
├── .env                  # Переменные окружения
├── requirements.txt      # Python зависимости
├── package.json         # Node.js зависимости
├── ecosystem.config.js  # Конфигурация PM2
├── seed_database.py     # Скрипт заполнения БД
└── README.md           # Документация
```

## 🗄 База данных

### Таблицы:

- **users** - пользователи из Telegram
- **questions** - вопросы для тестов
- **tests** - экземпляры тестов
- **test_answers** - ответы пользователей
- **test_results** - результаты тестов
- **payments** - платежи за пересдачи

### Управление базой данных:

```bash
# Просмотр БД в браузере
npx prisma studio

# Создание миграции
npx prisma migrate dev --name migration_name

# Сброс БД
npx prisma migrate reset
```

## 🎯 API Endpoints

### Пользователи
- `POST /api/users/` - создание пользователя
- `GET /api/users/{telegram_id}` - получение пользователя

### Вопросы
- `GET /api/questions/random` - 10 случайных вопросов
- `POST /api/questions/` - создание вопроса

### Тесты
- `POST /api/tests/start` - начало теста
- `POST /api/tests/{test_id}/answer` - отправка ответа
- `POST /api/tests/{test_id}/finish` - завершение теста
- `GET /api/tests/leaderboard` - таблица лидеров

### Telegram
- `POST /api/telegram/webhook` - webhook от Telegram
- `GET /api/telegram/payment/{user_id}/check` - проверка оплат

## 🔄 Управление процессами (PM2)

```bash
# Запуск в режиме разработки
npm run dev

# Запуск в production
npm run prod

# Остановка всех процессов
npm run stop

# Перезапуск
npm run restart

# Просмотр логов
npm run logs

# Мониторинг
pm2 monit
```

## 🐛 Отладка

### Логи

```bash
# Логи API
pm2 logs quiz-api

# Все логи
pm2 logs

# Очистка логов
pm2 flush
```

### Проверка статуса

```bash
# Статус процессов
pm2 status

# Информация о процессе
pm2 show quiz-api

# Использование ресурсов
pm2 monit
```

## 🚀 Деплой в production

### Подготовка сервера

1. Установите все зависимости
2. Настройте PostgreSQL
3. Получите SSL сертификат
4. Настройте nginx (опционально)

### Переменные окружения для production

```env
DEBUG=False
DATABASE_URL="postgresql://user:password@localhost:5432/quiz_app"
# Остальные настройки...
```

### Запуск

```bash
npm run prod
```

## 📞 Поддержка

При возникновении проблем:

1. Проверьте логи: `npm run logs`
2. Убедитесь, что PostgreSQL запущен
3. Проверьте правильность `.env` файла
4. Убедитесь, что все порты свободны
