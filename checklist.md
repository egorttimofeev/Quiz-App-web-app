# ✅ ЧЕКЛИСТ НАСТРОЙКИ .ENV

## 🚀 Быстрый старт (5 минут)

### 1. База данных PostgreSQL
- [ ] Установил PostgreSQL с https://postgresql.org/download/
- [ ] Создал базу данных `quiz_app`
- [ ] Запомнил пароль пользователя `postgres`
- [ ] Заменил в .env: `your_password` → мой пароль

### 2. Telegram Bot
- [ ] Написал @BotFather в Telegram
- [ ] Создал бота командой `/newbot`
- [ ] Скопировал токен в .env (формат: `1234567890:ABCdef...`)

### 3. Мой Telegram ID
- [ ] Написал @userinfobot в Telegram
- [ ] Отправил `/start`
- [ ] Скопировал свой ID в .env (только цифры)

### 4. Секретный ключ
**Вариант А (Python):**
- [ ] Выполнил: `python -c "import secrets; print(secrets.token_urlsafe(32))"`
- [ ] Скопировал результат в .env

**Вариант Б (вручную):**
- [ ] Придумал уникальную строку 20+ символов
- [ ] Пример: `my-quiz-app-secret-2024-random-string`

### 5. Telegram Stars
- [ ] Оставил `TELEGRAM_STARS_PROVIDER_TOKEN=""` пустым
- [ ] В @BotFather: `/mybots` → мой бот → `Payments` → `Telegram Stars`

---

## 🔧 Проверка настроек

```bash
# Автоматическая проверка
python check_config.py

# Настройка бота  
python setup_bot.py
```

---

## 📝 Итоговый .env должен выглядеть так:

```env
DATABASE_URL="postgresql://postgres:МОЙ_ПАРОЛЬ@localhost:5432/quiz_app"
TELEGRAM_BOT_TOKEN="1234567890:МОЙ_ТОКЕН_ОТ_BOTFATHER"  
TELEGRAM_ADMIN_ID="МОЙ_ТЕЛЕГРАМ_ID"
SECRET_KEY="МОЙ-СЛУЧАЙНЫЙ-СЕКРЕТНЫЙ-КЛЮЧ"
DEBUG=True
TELEGRAM_STARS_PROVIDER_TOKEN=""
API_PORT=8000
WEB_PORT=3000
```

---

## ❌ Частые ошибки

| Ошибка | Решение |
|--------|---------|
| `your_password` в .env | Замените на реальный пароль PostgreSQL |
| `your_telegram_bot_token` | Получите токен от @BotFather |
| `Connection refused` | Запустите PostgreSQL |
| `Invalid bot token` | Проверьте правильность токена |
| `Module not found` | Выполните `pip install -r requirements.txt` |

---

## 🎯 Готово к запуску?

Если все пункты отмечены ✅, запускайте:

```bash
# Windows
start.bat

# Linux/macOS  
./start.sh
```

Приложение откроется на http://localhost:8000