import logging
import json
import os
from fastapi import FastAPI, Request
from telegram import Update, KeyboardButton, ReplyKeyboardMarkup
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes

# Конфигурация
TOKEN = "7880774464:AAGBEe1pYDmT-NzWvVgKJBfyrCfj7mLSu8A"
WEBHOOK_URL = "https://basket-weaving-bot.onrender.com/webhook"
PORT = 10000

app = FastAPI()
bot = Application.builder().token(TOKEN).build()
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

# Хранилище пользователей (простое решение в памяти)
started_users = set()

# Генератор клавиатуры
def get_keyboard(user_id: int):
    buttons = [
        [KeyboardButton("Начать обучение")],
        [KeyboardButton("Магазин")],
        [KeyboardButton("Описание курса")]
    ]
    
    if user_id in started_users:
        buttons.insert(1, [KeyboardButton("Продолжить обучение")])
    
    return ReplyKeyboardMarkup(buttons, resize_keyboard=True)

# Обработчик /start
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.message.from_user.id
    await update.message.reply_text(
        "Привет!👋\n🌿🧺Добро пожаловать в мой обучающий чат-бот!\n\n"
        "⁉️Если у тебя есть вопросы или нужна дополнительная информация, просто напиши!\n"
        "💪🏻Давайте начнем учиться и создавать красивые вещи вместе!😊",
        reply_markup=get_keyboard(user_id)
    )

# Обработчик сообщений
async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.message.from_user.id
    text = update.message.text
    
    responses = {
        "Начать обучение": ("🚀 Обучение начато! Теперь доступно продолжение.", True),
        "Продолжить обучение": ("🔁 Продолжаем урок...", False),
        "Магазин": ("🛍️ Открываем магазин...", False),
        "Описание курса": ("📚 Курс по плетению корзин!\nПодробная инструкция...", False)
    }
    
    if text in responses:
        response_text, should_start = responses[text]
        if text == "Начать обучение":
            started_users.add(user_id)
        await update.message.reply_text(response_text, reply_markup=get_keyboard(user_id))
    else:
        await update.message.reply_text("❌ Неизвестная команда")

# Вебхук и остальной код остается без изменений
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
    # Сохраняем состояния
    with open("users.json", "w") as f:
        json.dump(list(started_users), f)
    
    # Останавливаем бота
    await bot.stop()
    await bot.shutdown()

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=PORT)