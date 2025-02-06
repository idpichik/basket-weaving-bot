from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, CallbackQueryHandler, CallbackContext

# Твой токен
TOKEN = '7880774464:AAGBEe1pYDmT-NzWvVgKJBfyrCfj7mLSu8A'

# Функция, которая будет отправлять приветственное сообщение и кнопки
async def start(update: Update, context: CallbackContext) -> None:
    # Создаем кнопки
    keyboard = [
        [InlineKeyboardButton("Материалы для плетения", callback_data='materials')],
        [InlineKeyboardButton("Начать обучение", callback_data='tutorial')],
        [InlineKeyboardButton("Помощь", callback_data='help')]
    ]
    
    # Создаем разметку для клавиатуры
    reply_markup = InlineKeyboardMarkup(keyboard)

    # Отправляем приветственное сообщение с кнопками
    welcome_text = ("Привет! Я бот для обучения плетению корзин.\n\n"
                    "В этом боте ты сможешь узнать:\n"
                    "1. Какие материалы нужны для плетения корзин\n"
                    "2. Как начать обучение\n"
                    "3. Где найти полезные ресурсы\n"
                    "Выберите одну из опций ниже, чтобы начать.")

    await update.message.reply_text(welcome_text, reply_markup=reply_markup)

# Функция для обработки нажатий кнопок
async def button(update: Update, context: CallbackContext) -> None:
    query = update.callback_query
    # Получаем данные, переданные в callback_data
    choice = query.data

    if choice == 'materials':
        response_text = "Для плетения корзин тебе понадобятся:\n- Лоза или прутья\n- Ножницы\n- Клей (по желанию)"
    elif choice == 'tutorial':
        response_text = "Ты можешь начать обучение плетению корзин с самого простого уровня.\n1. Собери материалы\n2. Ознакомься с базовыми техниками\n3. Начни плести первую корзину!"
    elif choice == 'help':
        response_text = "Вот что ты можешь сделать:\n/start - Запуск бота\n/help - Получить информацию о боте\n/materials - Узнать о материалах для плетения\n/tutorial - Начать обучение плетению корзин"
    
    # Ответ на нажатие кнопки
    await query.answer()
    await query.edit_message_text(text=response_text)

# Основная функция
def main():
    # Создаем объект приложения
    app = ApplicationBuilder().token(TOKEN).build()

    # Добавляем обработчики команд
    app.add_handler(CommandHandler("start", start))  # Срабатывает при вводе команды /start
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
