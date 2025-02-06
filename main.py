from telegram import KeyboardButton, ReplyKeyboardMarkup
from telegram.ext import Application, CommandHandler, MessageHandler, filters

TOKEN = '7880774464:AAGBEe1pYDmT-NzWvVgKJBfyrCfj7mLSu8A'

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

def main():
    # Инициализация бота
    app = Application.builder().token(TOKEN).build()

    # Обработчик команды /start
    app.add_handler(CommandHandler("start", start))

    # Обработчик нажатия на кнопки
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, button_click))

    # Запуск бота
    app.run_polling()

if __name__ == '__main__':
    main()
