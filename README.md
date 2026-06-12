# 📝 Quiz App - Telegram Web App

Веб-приложение для проведения тестов с интеграцией в Telegram, построенное на современном стеке технологий.

![Python](https://img.shields.io/badge/Python-FastAPI-3776ab?style=for-the-badge&logo=python&logoColor=white)
![Node.js](https://img.shields.io/badge/Node.js-Frontend-339933?style=for-the-badge&logo=node.js&logoColor=white)
![PostgreSQL](https://img.shields.io/badge/PostgreSQL-Database-336791?style=for-the-badge&logo=postgresql&logoColor=white)
![Telegram](https://img.shields.io/badge/Telegram-Integration-0088cc?style=for-the-badge&logo=telegram&logoColor=white)

---

## 🎯 Функциональность

- ✅ Приветственный экран с информацией о тесте
- ✅ Переключение темы (светлая/темная)
- ✅ Тест из 10 вопросов с 4 вариантами ответов
- ✅ Таймер и счетчик вопросов
- ✅ Навигация между вопросами
- ✅ Результаты с детализацией ошибок
- ✅ Таблица лидеров с результатами всех пользователей
- ✅ Система оплаты пересдач (200 Telegram Stars)
- ✅ Случайная выборка вопросов из базы (50+ вопросов)
- ✅ Автоматическое сохранение пользователей из Telegram
- ✅ Ссылка на админа для предложений

---

## 📋 Правила тестирования

- **10 вопросов** в тесте
- **4 варианта** ответа на каждый вопрос
- **1 правильный** ответ
- **7+ правильных** ответов для прохождения
- **Первое прохождение** бесплатное
- **Пересдачи** за 200 Telegram Stars

---

## 🛠 Технологический стек

**Backend:**
- Python 3.8+
- FastAPI
- PostgreSQL
- ORM: Prisma

**Frontend:**
- HTML5 + CSS3
- JavaScript (Vanilla)
- Telegram Web App API

**DevOps:**
- PM2 (Process Manager)
- Node.js 16+

---

## 📁 Структура проекта

```
web-app/
├── api/                    # Backend API (FastAPI)
│   ├── main.py            # Главный файл
│   ├── models/            # Модели данных
│   ├── routes/            # API маршруты
│   │   ├── users.py
│   │   ├── questions.py
│   │   ├── tests.py
│   │   └── telegram.py
│   └── services/          # Сервисы
├── web-app/               # Frontend
│   ├── templates/         # HTML шаблоны
│   └── static/           # Статические файлы
│       ├── css/
│       └── js/
├── prisma/               # Схема БД
├── requirements.txt      # Python зависимости
├── package.json         # Node.js зависимости
└── ecosystem.config.js  # PM2 конфигурация
```

---

## 💾 База данных

Основные таблицы:

- **users** — пользователи из Telegram
- **questions** — вопросы для тестов
- **tests** — экземпляры тестов
- **test_answers** — ответы пользователей
- **test_results** — результаты тестов
- **payments** — платежи за пересдачи

---

## 🚀 Быстрый старт

### Предварительные требования

1. **Python 3.8+**
2. **Node.js 16+**
3. **PostgreSQL 12+** (создайте БД `quiz_app`)
4. **PM2** (глобально): `npm install -g pm2`

### Установка и запуск

1. **Клонирование**:
```bash
git clone <repository-url>
cd web-app
```

2. **Настройка `.env`**:
```env
DATABASE_URL="postgresql://postgres:password@localhost:5432/quiz_app"
TELEGRAM_BOT_TOKEN="your_token"
TELEGRAM_ADMIN_ID="your_admin_id"
SECRET_KEY="your_secret_key"
API_PORT=8000
WEB_PORT=3000
DEBUG=True
```

3. **Автоматический запуск**:

Windows:
```bash
start.bat
```

Linux/macOS:
```bash
chmod +x start.sh
./start.sh
```

Или вручную:
```bash
# Python зависимости
pip install -r requirements.txt

# Node.js зависимости
npm install

# Миграции БД
npx prisma migrate deploy

# Заполнение БД
python seed_database.py

# Запуск в разработке
npm run dev
```

---

## 🔧 Управление процессами (PM2)

```bash
npm run dev      # Разработка
npm run prod     # Production
npm run stop     # Остановка
npm run restart  # Перезапуск
npm run logs     # Логи
```

---

## 🎮 API Endpoints

**Пользователи:**
- `POST /api/users/` — создание пользователя
- `GET /api/users/{telegram_id}` — получение пользователя

**Вопросы:**
- `GET /api/questions/random` — 10 случайных вопросов
- `POST /api/questions/` — создание вопроса

**Тесты:**
- `POST /api/tests/start` — начало теста
- `POST /api/tests/{test_id}/answer` — отправка ответа
- `POST /api/tests/{test_id}/finish` — завершение теста
- `GET /api/tests/leaderboard` — таблица лидеров

**Telegram:**
- `POST /api/telegram/webhook` — webhook от Telegram
- `GET /api/telegram/payment/{user_id}/check` — проверка оплат

---

## 🔒 Настройка Telegram Bot

1. Напишите [@BotFather](https://t.me/BotFather) в Telegram
2. Создайте бота: `/newbot`
3. Получите токен и добавьте в `.env`
4. Используйте `/setmenubutton` для Web App
5. Укажите URL вашего приложения

---

## 📊 Управление базой данных

```bash
# Просмотр БД в браузере
npx prisma studio

# Создание миграции
npx prisma migrate dev --name migration_name

# Сброс БД
npx prisma migrate reset
```

---

## 🐛 Отладка

```bash
# Статус процессов
pm2 status

# Просмотр логов
pm2 logs quiz-api

# Мониторинг ресурсов
pm2 monit

# Информация о процессе
pm2 show quiz-api
```
