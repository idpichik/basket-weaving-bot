from telegram import Update
from telegram.ext import Updater, CommandHandler, CallbackContext

# Вставь сюда свой токен, который ты получил от BotFather
TOKEN = '7880774464:AAGBEe1pYDmT-NzWvVgKJBfyrCfj7mLSu8A'

# Функция, которая будет вызываться при команде /start
def start(update: Update, context: CallbackContext) -> None:
    update.message.reply_text('Привет! Я бот для обучения плетению корзин.')

# Основная функция, которая запускает бота
def main():
    # Создаем объект Updater с твоим токеном
    updater = Updater(TOKEN)
    updater = Updater(7880774464:AAGBEe1pYDmT-NzWvVgKJBfyrCfj7mLSu8A)

    # Получаем диспетчер, чтобы добавить обработчики команд
    dispatcher = updater.dispatcher

    # Добавляем обработчик для команды /start
    dispatcher.add_handler(CommandHandler('start', start))

    # Запускаем бота
    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()
