# 🤖 Настройка Telegram Web App для Quiz Master

## Шаг 1: Создание Telegram бота

1. **Откройте Telegram** и найдите бота **@BotFather**
2. **Отправьте команду** `/newbot`
3. **Введите название** бота (например: "Quiz Master Bot")
4. **Введите username** бота (например: "quiz_master_your_name_bot")
   - Username должен заканчиваться на "bot"
   - Должен быть уникальным
5. **Сохраните TOKEN** - это важно для API!

## Шаг 2: Настройка Web App

После создания бота отправьте BotFather следующие команды:

### Установить кнопку меню
```
/setmenubutton
[выберите вашего бота]
```
- **Текст кнопки:** 🎯 Начать квиз
- **URL:** `http://localhost:8000/app` (для тестирования)

### Установить описание бота
```
/setdescription
[выберите вашего бота]
```
**Описание:**
```
🎯 Quiz Master - интерактивный квиз-бот!

✨ Возможности:
• 10 вопросов с вариантами ответов
• Таймер на 5 минут
• Система оценок и статистика
• Повторное прохождение за Telegram Stars
• Таблица лидеров

🚀 Нажми кнопку меню чтобы начать!
```

### Установить краткое описание
```
/setabouttext
[выберите вашего бота]
```
**Краткое описание:**
```
🎯 Интерактивный квиз-бот с системой оценок и оплатой через Telegram Stars
```

### Установить команды
```
/setcommands
[выберите вашего бота]
```
**Команды:**
```
start - 🚀 Начать квиз
help - ℹ️ Помощь
stats - 📊 Моя статистика
leaderboard - 🏆 Таблица лидеров
```

## Шаг 3: Настройка .env файла

Создайте файл `.env` в корне проекта:

```env
# Telegram Bot Settings
TELEGRAM_BOT_TOKEN=ваш_токен_бота_здесь
TELEGRAM_BOT_USERNAME=ваш_username_бота

# Database Settings
DATABASE_URL=sqlite:///quiz_app.db

# App Settings
APP_HOST=localhost
APP_PORT=8000
APP_URL=http://localhost:8000

# Security
SECRET_KEY=ваш_секретный_ключ_здесь

# Telegram Stars (для оплаты)
STARS_PROVIDER_TOKEN=ваш_провайдер_токен
RETRY_COST_STARS=200

# Development
DEBUG=true
```

## Шаг 4: Тестирование

### Локальное тестирование
1. Запустите сервер: `.\run_server.bat`
2. Откройте в браузере: `http://localhost:8000/app`
3. Проверьте функциональность

### Тестирование в Telegram
1. Для тестирования нужен публичный URL (ngrok, localtunnel и т.д.)
2. Установите ngrok: `npm install -g ngrok`
3. Запустите туннель: `ngrok http 8000`
4. Обновите URL в BotFather на полученный ngrok URL

## Шаг 5: Деплой для продакшена

### Варианты хостинга:
1. **Railway** - бесплатный хостинг с автодеплоем
2. **Heroku** - классический вариант
3. **DigitalOcean App Platform** - простой и надежный
4. **Vercel** - для статики + serverless функций

### Настройка домена:
1. Получите бесплатный домен или используйте поддомен
2. Обновите URL в BotFather на ваш домен
3. Обновите переменную `APP_URL` в `.env`

## Шаг 6: Интеграция с Telegram Stars

Для функции оплаты повторных попыток:

```javascript
// В коде бота (дополнительно)
async function createPaymentLink(userId, testId) {
    const invoice = {
        title: "Повторное прохождение квиза",
        description: "Дополнительная попытка пройти тест",
        payload: `retry_${testId}_${userId}`,
        currency: "XTR", // Telegram Stars
        prices: [{ label: "Повтор теста", amount: 200 }]
    };
    
    return await bot.api.createInvoiceLink(invoice);
}
```

## Полезные команды BotFather:

- `/mybots` - управление ботами
- `/setname` - изменить имя бота
- `/setdescription` - изменить описание
- `/setuserpic` - установить аватар
- `/setcommands` - установить команды
- `/deletebot` - удалить бота

## Дополнительные возможности:

### Inline режим
```
/setinline
[выберите вашего бота]
Placeholder: Поделиться квизом...
```

### Группы и каналы
```
/setjoingroups
[выберите вашего бота]
Enable - для разрешения добавления в группы
```

### Webhook (для продакшена)
```python
# Установка webhook
webhook_url = "https://ваш-домен.com/webhook"
await bot.api.set_webhook(webhook_url)
```

## Troubleshooting:

1. **Бот не отвечает** - проверьте TOKEN
2. **Web App не открывается** - проверьте URL
3. **Кнопка меню не видна** - переустановите через /setmenubutton
4. **Ошибки CORS** - добавьте домен в настройки CORS

## Контакты для поддержки:
- Telegram: @your_support_bot
- Email: support@yourdomain.com

---
*Создано для Quiz Master Bot - интерактивная платформа для квизов с интеграцией Telegram Stars*