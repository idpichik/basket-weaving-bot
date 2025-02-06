from flask import Flask, request
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters
import logging

app = Flask(__name__)

TOKEN = '7880774464:AAGBEe1pYDmT-NzWvVgKJBfyrCfj7mLSu8A''

# Инициализация Telegram бота
telegram_bot = Application.builder().token(TOKEN).build()

# Приветственное сообщение с кнопками меню
async def start(update, context):
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
async def button_click(update, context):
    user_input = update.message.text

    if user_input == "Начать обучение":
        await update.message.reply_text("Вы начали обучение!")
    elif user_input == "Продолжить обучение":
        await update.message.reply_text("Вы продолжили обучение!")
    elif user_input == "Магазин":
        await update.message.reply_text("Открываем магазин...")
    elif user_input == "Описание курса":
        await update.message.reply_text("Описание курса: \nЭтот курс поможет вам...")

# Вебхук для обработки сообщений от Telegram
@app.route('/webhook', methods=['POST'])
def webhook():
    json_str = request.get_data(as_text=True)  # Получаем данные как строку
    update = Update.de_json(json.loads(json_str), telegram_bot.bot)  # Преобразуем строку в словарь
    telegram_bot.process_new_updates([update])
    return 'OK'

def main():
    # Настройка вебхука
    webhook_url = 'https://basket-weaving-bot.onrender.com/webhook'
    telegram_bot.bot.set_webhook(url=webhook_url)

    # Запуск Flask-приложения
    app.run(host='0.0.0.0', port=10000)

if __name__ == '__main__':
    main()
