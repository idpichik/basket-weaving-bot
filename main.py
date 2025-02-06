import json
import os
import logging
from fastapi import FastAPI, Request
from telegram import Update, KeyboardButton, ReplyKeyboardMarkup
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes

# Конфигурация
TOKEN = "7880774464:AAGBEe1pYDmT-NzWvVgKJBfyrCfj7mLSu8A"
WEBHOOK_URL = "https://basket-weaving-bot.onrender.com/webhook"
PORT = 10000

app = FastAPI()
bot = Application.builder().token(TOKEN).build()

# Загрузка состояний пользователей
if os.path.exists("users.json"):
    with open("users.json", "r") as f:
        started_users = set(json.load(f))
else:
    started_users = set()

# Логирование
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO
)

def get_keyboard(user_id: int):
    """Генерирует клавиатуру в зависимости от состояния"""
    if user_id in started_users:
        # После начала обучения
        return ReplyKeyboardMarkup(
            [
                [KeyboardButton("Продолжить обучение")],
                [KeyboardButton("Начать сначала")]  # Новая кнопка внизу
            ],
            resize_keyboard=True
        )
    else:
        # До начала обучения
        return ReplyKeyboardMarkup(
            [
                [KeyboardButton("Начать обучение")],
                [KeyboardButton("Магазин")],
                [KeyboardButton("Описание курса")]
            ],
            resize_keyboard=True
        )

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.message.from_user.id
    await update.message.reply_text(
        "Привет!👋\n🌿🧺Добро пожаловать в мой обучающий чат-бот!\n\n"
        "⁉️Если у тебя есть вопросы или нужна дополнительная информация, просто напиши!\n"
        "💪🏻Давайте начнем учиться и создавать красивые вещи вместе!😊",
        reply_markup=get_keyboard(user_id)
    )

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.message.from_user.id
    text = update.message.text

    if text == "Начать обучение":
        started_users.add(user_id)
        await update.message.reply_text(
            "🚀 Обучение начато! Выберите действие:",
            reply_markup=get_keyboard(user_id)
        )

    elif text == "Начать сначала":
        started_users.discard(user_id)
        await update.message.reply_text(
            "🔄 Обучение сброшено! Начните заново:",
            reply_markup=get_keyboard(user_id)
        )

    elif text == "Продолжить обучение":
        if user_id in started_users:
            await update.message.reply_text("➡️ Продолжаем урок...")
        else:
            await update.message.reply_text(
                "⚠️ Сначала начните обучение!",
                reply_markup=get_keyboard(user_id)
            )

    elif text == "Магазин":
        await update.message.reply_text("🛍️ Магазин временно закрыт")

    elif text == "Описание курса":
        await update.message.reply_text(
            "📚 Курс по плетению корзин!\n"
            "Подробная инструкция шаг за шагом!"
        )

    else:
        await update.message.reply_text("❌ Неизвестная команда")

@app.post("/webhook")
async def webhook(request: Request):
    try:
        data = await request.json()
        update = Update.de_json(data, bot.bot)
        await bot.process_update(update)
        return {"status": "ok"}
    except Exception as e:
        logging.error(f"Ошибка: {e}")
        return {"status": "error"}

@app.on_event("startup")
async def init():
    await bot.initialize()
    await bot.bot.set_webhook(WEBHOOK_URL)
    bot.add_handler(CommandHandler("start", start))
    bot.add_handler(MessageHandler(filters.TEXT, handle_message))
    await bot.start()

@app.on_event("shutdown")
async def shutdown():
    with open("users.json", "w") as f:
        json.dump(list(started_users), f)
    await bot.stop()
    await bot.shutdown()

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=PORT)