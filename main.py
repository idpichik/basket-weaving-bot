import logging
from flask import Flask, request
from telegram import Update, KeyboardButton, ReplyKeyboardMarkup
from telegram.ext import Application, CommandHandler, MessageHandler, filters
import os
import asyncio

TOKEN = '7880774464:AAGBEe1pYDmT-NzWvVgKJBfyrCfj7mLSu8A'

app = Flask(__name__)

# Инициализация Telegram бота
telegram_bot = Application.builder().token(TOKEN).build()

# Приветственное сообщение с кнопками меню
async def start(update: Update, context):
    # Кнопки для меню
    keyboard = [
        [KeyboardButton("Начать обучение")],
        [KeyboardButton("Продолжить обучение")],
        [KeyboardButton("Магазин")],
        [KeyboardButton("Описание курса")]
    ]
    reply_markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True)

    # Отправка приветственного сообщения с кнопками
    await update.message.reply_text(
        "Привет! Я обучающий бот. Выберите один из вариантов ниже:",
        reply_markup=reply_markup
    )

# Обработчик кнопок
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

# Добавление команд в бота
def setup_bot():
    telegram_bot.add_handler(CommandHandler("start", start))
    telegram_bot.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, button_click))

# Вебхук обработчик
@app.route('/webhook', methods=['POST'])
def webhook():
    json_str = request.get_data().decode('UTF-8')
    update = Update.de_json(json_str, telegram_bot.bot)
    telegram_bot.process_update(update)
    return 'OK'

async def set_webhook():
    # Устанавливаем вебхук асинхронно
    webhook_url = 'https://basket-weaving-bot.onrender.com/webhook'  # Замените на ваш реальный URL
    await telegram_bot.bot.set_webhook(url=webhook_url)

@app.before_first_request
def before_first_request():
    # Устанавливаем вебхук перед первым запросом
    asyncio.run(set_webhook())

if __name__ == "__main__":
    # Настроим сервер Flask для обработки вебхуков
    setup_bot()
    app.run(host='0.0.0.0', port=10000)  # Порт 10000 для Render
