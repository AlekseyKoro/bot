from telegram import Update
from telegram.ext import Updater, CommandHandler, CallbackContext
import logging
import config
import database
import utils
import gpt_model  # Подключение модуля с GPT

# Настройка логирования
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)

# Функции команд
def start(update: Update, context: CallbackContext):
    update.message.reply_text('Здравствуйте! Я ваш бизнес-бот. Чем могу помочь?')

def help_command(update: Update, context: CallbackContext):
    update.message.reply_text('Команды: /start - начать, /help - помощь')

def get_report(update: Update, context: CallbackContext):
    # Пример запроса отчета из базы данных
    conn = database.connect_db()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM reports')
    reports = cursor.fetchall()
    conn.close()

    if reports:
        for report in reports:
            update.message.reply_text(f"Отчет {report[0]}: {report[1]}\n{report[2]}")
    else:
        update.message.reply_text('Отчеты не найдены.')

def analyze(update: Update, context: CallbackContext):
    # Пример анализа данных
    data = "Данные для анализа"
    result = utils.analyze_data(data)
    update.message.reply_text(result)

def recommend(update: Update, context: CallbackContext):
    # Пример генерации рекомендаций
    data = "Данные для рекомендаций"
    recommendations = utils.generate_recommendations(data)
    update.message.reply_text(recommendations)

def gpt_query(update: Update, context: CallbackContext):
    user_input = ' '.join(context.args)
    if not user_input:
        update.message.reply_text('Введите запрос для GPT.')
        return

    response = gpt_model.get_gpt_response(user_input)
    update.message.reply_text(response)

def main():
    # Создание и настройка бота
    updater = Updater(token=config.TOKEN, use_context=True)
    dp = updater.dispatcher

    # Добавление обработчиков команд
    dp.add_handler(CommandHandler('start', start))
    dp.add_handler(CommandHandler('help', help_command))
    dp.add_handler(CommandHandler('get_report', get_report))
    dp.add_handler(CommandHandler('analyze', analyze))
    dp.add_handler(CommandHandler('recommend', recommend))
    dp.add_handler(CommandHandler('gpt_query', gpt_query))  # Обработка запросов к GPT

    # Запуск бота
    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    database.create_tables()
    main()
