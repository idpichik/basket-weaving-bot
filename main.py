from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes

# Вставь сюда свой токен
TOKEN = '7880774464:AAGBEe1pYDmT-NzWvVgKJBfyrCfj7mLSu8A'

# Функция, которая будет вызываться при команде /start
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text('Привет! Я бот для обучения плетению корзин.')

# Основная функция, которая запускает бота
def main():
    # Создаем объект приложения
    app = ApplicationBuilder().token(TOKEN).build()

    # Добавляем обработчик для команды /start
    app.add_handler(CommandHandler('start', start))

    # Запускаем бота
    print("Бот запущен и готов к работе!")
    app.run_polling()

if __name__ == '__main__':
    main()
