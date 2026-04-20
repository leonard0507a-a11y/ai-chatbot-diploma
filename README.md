# Телеграм-бот технической поддержки на базе GPT

## Функционал
- Запоминает пользователей
- Хранит историю диалога в PostgreSQL
- Работает 24/7 на Railway
- Использует GPT-4o-mini для генерации ответов

## Технологии
- Python + python-telegram-bot
- OpenAI API
- PostgreSQL + SQLAlchemy
- Railway (деплой)

## Переменные окружения
- `TELEGRAM_TOKEN` — токен бота
- `OPENAI_API_KEY` — ключ OpenAI
- `DATABASE_URL` — строка подключения к PostgreSQL (выдаётся Railway)