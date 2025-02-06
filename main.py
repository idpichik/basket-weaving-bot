from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes

# Вставь сюда свой токен
TOKEN = '7880774464:AAGBEe1pYDmT-NzWvVgKJBfyrCfj7mLSu8A'

# Функция для команды /start
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text('Привет! Я бот для обучения плетению корзин.')

# Функция для команды /help
async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    help_text = (
        "Я бот для обучения плетению корзин.\n"
        "Вот что ты можешь сделать:\n"
        "/start - Запуск бота\n"
        "/help - Получить информацию о боте\n"
        "/materials - Узнать о материалах для плетения\n"
        "/tutorial - Начать обучение плетению корзин"
    )
    await update.message.reply_text(help_text)

# Функция для команды /materials
async def materials(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    materials_text = (
        "Для плетения корзин тебе понадобятся:\n"
        "- Лоза или прутья\n"
        "- Ножницы\n"
        "- Клей (по желанию)"
    )
    await update.message.reply_text(materials_text)

# Функция для команды /tutorial
async def tutorial(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    tutorial_text = (
        "Ты можешь начать обучение плетению корзин с самого простого уровня.\n"
        "Вот шаги:\n"
        "1. Собери материалы\n"
        "2. Ознакомься с базовыми техниками\n"
        "3. Начни плести первую корзину!"
    )
    await update.message.reply_text(tutorial_text)

# Основная функция
def main():
    app = ApplicationBuilder().token(TOKEN).build()

    # Добавляем обработчики команд
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("help", help_command))
    app.add_handler(CommandHandler("materials", materials))
    app.add_handler(CommandHandler("tutorial", tutorial))

    # Запускаем webhook
    app.run_webhook(
        listen="0.0.0.0", 
        port=8443,
        url_path=TOKEN,
        webhook_url=f"https://basket-weaving-bot.onrender.com/{TOKEN}"
    )

if __name__ == '__main__':
    main()
