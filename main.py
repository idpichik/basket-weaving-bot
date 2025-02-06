import os
import json
from flask import Flask, request
from telegram import KeyboardButton, ReplyKeyboardMarkup, Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters
from telegram import Bot

# Инициализация Flask приложения
app = Flask(__name__)

# Ваш токен для бота
TOKEN = '7880774464:AAGBEe1pYDmT-NzWvVgKJBfyrCfj7mLSu8A'

# Создаем объект приложения для бота
application = Application.builder().token(TOKEN).build()

# Приветственное сообщение с кнопками меню
async def start(update, context):
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

# Обработчики команд для кнопок
async def button_click(update, context):
    # Узнаем, какая кнопка была нажата
    user_input = update.message.text

    if user_input == "Начать обучение":
        await update.message.reply_text("Вы начали обучение!")
    elif user_input == "Продолжить обучение":
        await update.message.reply_text("Вы продолжили обучение!")
    elif user_input == "Магазин":
        await update.message.reply_text("Открываем магазин...")
    elif user_input == "Описание курса":
        await update.message.reply_text("Описание курса: \nЭтот курс поможет вам...")

# Вебхук для обработки входящих запросов
@app.route('/webhook', methods=['POST'])
def webhook():
    # Получаем данные запроса
    json_str = request.get_data().decode('UTF-8')
    
    # Преобразуем JSON данные в объект Update
    update = Update.de_json(json.loads(json_str), application.bot)
    
    # Передаем обновление в обработчик
    application.update_queue.put(update)
    
    return 'ok', 200

# Устанавливаем вебхук
application.bot.set_webhook(url='https://YOUR_RENDER_APP_URL/webhook')

def main():
    # Обработчик команды /start
    application.add_handler(CommandHandler("start", start))

    # Обработчик нажатия на кнопки
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, button_click))

    # Запуск Flask приложения
    port = int(os.environ.get('PORT', 5000))  # Получаем порт из переменных окружения
    app.run(host='0.0.0.0', port=port)

if __name__ == '__main__':
    main()
