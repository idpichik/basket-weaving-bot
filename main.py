from fastapi import FastAPI, Request
from pydantic import BaseModel
from telegram import Update, KeyboardButton, ReplyKeyboardMarkup
from telegram.ext import Application, CommandHandler, MessageHandler, filters
import json
import logging
import uvicorn

app = FastAPI()

TOKEN = '7880774464:AAGBEe1pYDmT-NzWvVgKJBfyrCfj7mLSu8A'

# Инициализация Telegram бота
telegram_bot = Application.builder().token(TOKEN).build()

# Приветственное сообщение с кнопками меню
async def start(update: Update, context):
    keyboard = [
        [KeyboardButton("Начать обучение")],
        [KeyboardButton("Продолжить обучение")],
        [KeyboardButton("Магазин")],
        [KeyboardButton("Описание курса")]
    ]
    reply_markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True)

    await update.message.reply_text(
        "Привет! Я обучающий бот. Выберите один из вариантов ниже:",
        reply_markup=reply_markup
    )

# Обработчики команд для кнопок
async def button_click(update: Update, context):
    user_input = update.message.text

    if user_input == "Начать обучение":
        await update.message.reply_text("Вы начали обучение!")
    elif user_input == "Продолжить обучение":
        await update.message.reply_text("Вы продолжили обучение!")
    elif user_input == "Магазин":
        await update.message.reply_text("Открываем магазин...")
    elif user_input == "Описание курса":
        await update.message.reply_text("Описание курса: \nЭтот курс поможет вам...")

# Регистрация обработчиков
telegram_bot.add_handler(CommandHandler("start", start))
telegram_bot.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, button_click))

# Синхронный вебхук для обработки сообщений от Telegram
@app.post("/webhook")
async def webhook(request: Request):
    data = await request.json()
    update = Update.de_json(data, telegram_bot.bot)
    await telegram_bot.process_update(update)
    return {"status": "ok"}

# Настройка вебхука
async def set_webhook():
    webhook_url = 'https://basket-weaving-bot.onrender.com/webhook'
    await telegram_bot.bot.set_webhook(url=webhook_url)

@app.on_event("startup")
async def on_startup():
    await set_webhook()
    await telegram_bot.initialize()

if __name__ == '__main__':
    uvicorn.run(app, host="0.0.0.0", port=8000)