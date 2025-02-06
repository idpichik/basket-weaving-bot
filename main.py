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

# Логирование
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO
)

# Клавиатура
def get_keyboard():
    return ReplyKeyboardMarkup([
        [KeyboardButton("Начать обучение")],
        [KeyboardButton("Продолжить обучение")],
        [KeyboardButton("Магазин")],
        [KeyboardButton("Описание курса")]
    ], resize_keyboard=True)

# Команды
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "Привет!👋\n🌿🧺Добро пожаловать в мой обучающий чат-бот! Здесь можно получить все необходимые материалы и инструкции по плетению корзин. Я подготовил пошаговые видеоуроки, советы и рекомендации, чтобы процесс обучения был простым и увлекательным.\n⁉️Если у тебя есть вопросы или нужна дополнительная информация, просто напиши — я всегда на связи!\n💪🏻Давайте начнем учиться и создавать красивые вещи вместе!😊",
        reply_markup=get_keyboard()
    )

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text
    response = {
        "Начать обучение": "🚀 Начинаем обучение!",
        "Продолжить обучение": "🔁 Продолжаем урок...",
        "Магазин": "🛍️ Открываем магазин...",
        "Описание курса": "📚 Курс по плетению корзин!"
    }.get(text, "❌ Неизвестная команда")
    
    await update.message.reply_text(response)

# Вебхук
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

# Инициализация
@app.on_event("startup")
async def init():
    await bot.initialize()
    await bot.bot.set_webhook(WEBHOOK_URL)
    bot.add_handler(CommandHandler("start", start))
    bot.add_handler(MessageHandler(filters.TEXT, handle_message))
    await bot.start()

@app.on_event("shutdown")
async def shutdown():
    await bot.stop()
    await bot.shutdown()

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=PORT)