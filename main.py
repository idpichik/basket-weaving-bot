import os
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes

# Токен Telegram-бота
TOKEN = '7880774464:AAGBEe1pYDmT-NzWvVgKJBfyrCfj7mLSu8A'

# Функция, которая будет вызываться при команде /start
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text('Привет! Я бот для обучения плетению корзин.')

# Основная функция
def main():
    # Создаём объект приложения
    app = ApplicationBuilder().token(TOKEN).build()

    # Добавляем обработчик для команды /start
    app.add_handler(CommandHandler('start', start))

    # Определяем порт для вебсервиса (Render задаёт порт через переменную окружения PORT)
    port = int(os.environ.get('PORT', 8443))

    # Настраиваем webhook
    app.run_webhook(
        listen="0.0.0.0",  # Слушаем на всех интерфейсах
        port=port,         # Порт из переменной окружения
        url_path=TOKEN,    # Путь для вебхука
        webhook_url=f"https://{os.environ['RENDER_EXTERNAL_HOSTNAME']}/{TOKEN}"  # URL для Telegram
    )

if __name__ == '__main__':
    main()
