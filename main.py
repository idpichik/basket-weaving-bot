from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup, ReplyKeyboardMarkup, KeyboardButton
from telegram.ext import ApplicationBuilder, CommandHandler, CallbackQueryHandler, CallbackContext

# Твой токен
TOKEN = '7880774464:AAGBEe1pYDmT-NzWvVgKJBfyrCfj7mLSu8A'

# Функция для создания кнопок с меню
async def show_main_menu(update: Update, context: CallbackContext) -> None:
    # Кнопки для основного меню
    keyboard = [
        [InlineKeyboardButton("Команды", callback_data='commands')],
        [InlineKeyboardButton("Меню", callback_data='menu')]
    ]
    
    reply_markup = InlineKeyboardMarkup(keyboard)

    welcome_text = "Привет! Я бот для обучения плетению корзин. Выберите одно из действий ниже."

    # Отправляем сообщение с кнопками
    await update.message.reply_text(welcome_text, reply_markup=reply_markup)

# Функция для обработки нажатий кнопок
async def button(update: Update, context: CallbackContext) -> None:
    query = update.callback_query
    choice = query.data

    if choice == 'commands':
        # Покажем список команд
        response_text = "/start - Начать обучение\n/materials - Материалы для плетения\n/tutorial - Инструкция по плетению"
        await query.edit_message_text(text=response_text)

    elif choice == 'menu':
        # Покажем основное меню с действиями
        keyboard = [
            [InlineKeyboardButton("Начать обучение", callback_data='start_tutorial')],
            [InlineKeyboardButton("Магазин", callback_data='shop')],
            [InlineKeyboardButton("Продолжить обучение", callback_data='continue_tutorial')],
            [InlineKeyboardButton("Описание курса", callback_data='course_description')]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)

        response_text = "Выберите одну из следующих опций:"
        await query.edit_message_text(text=response_text, reply_markup=reply_markup)

    elif choice == 'start_tutorial':
        # Начало обучения
        response_text = "Прекрасно! Начинаем обучение плетению корзин!"
        await query.edit_message_text(text=response_text)

    elif choice == 'shop':
        # Магазин
        response_text = "Добро пожаловать в магазин! Что бы вы хотели купить?"
        await query.edit_message_text(text=response_text)

    elif choice == 'continue_tutorial':
        # Продолжение обучения
        response_text = "Продолжаем обучение. Выберите, что бы вы хотели изучить."
        await query.edit_message_text(text=response_text)

    elif choice == 'course_description':
        # Описание курса
        response_text = "Этот курс поможет вам научиться плести корзины. Он состоит из нескольких уроков по техникам плетения."
        await query.edit_message_text(text=response_text)

# Основная функция
def main():
    # Создаем объект приложения
    app = ApplicationBuilder().token(TOKEN).build()

    # Добавляем обработчики команд
    app.add_handler(CommandHandler("start", show_main_menu))  # Срабатывает при вводе команды /start
    app.add_handler(CallbackQueryHandler(button))  # Обработка нажатий кнопок

    # Запускаем webhook (если используешь Render или другую платформу с webhook)
    app.run_webhook(
        listen="0.0.0.0", 
        port=8443,
        url_path=TOKEN,
        webhook_url=f"https://basket-weaving-bot.onrender.com/{TOKEN}"
    )

if __name__ == '__main__':
    main()
