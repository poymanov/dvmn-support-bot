import os
import logging
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
from dialog_flow import get_answer
from tg_logger import set_logger

TELEGRAM_BOT_TOKEN = os.environ['TELEGRAM_BOT_TOKEN']

logger = logging.getLogger(__file__)


def start_command_handler(update, context):
    context.bot.send_message(chat_id=update.effective_chat.id, text='Здравствуйте! Чем можем помочь?')


def answer_handler(update, context):
    answer = get_answer(update.message.text, 'tg-{}'.format(update.effective_chat.id), True)
    context.bot.send_message(chat_id=update.effective_chat.id, text=answer)


def error_handler(update, context):
    logger.exception('Telegram-бот упал с ошибкой')


def start_bot():
    updater = Updater(token=TELEGRAM_BOT_TOKEN)
    dispatcher = updater.dispatcher
    updater.start_polling()

    start_handler = CommandHandler('start', start_command_handler)
    dispatcher.add_handler(start_handler)

    echo_handler = MessageHandler(Filters.text & (~Filters.command), answer_handler)
    dispatcher.add_handler(echo_handler)

    dispatcher.add_error_handler(error_handler)


def main():
    set_logger(logger)

    start_bot()
    logger.warning('Telegram-бот запущен')


if __name__ == '__main__':
    main()
