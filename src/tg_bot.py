import os
import logging
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
import telegram
from dialog_flow import get_answer

TELEGRAM_BOT_TOKEN = os.environ['TELEGRAM_BOT_TOKEN']
TELEGRAM_LOGGER_BOT_TOKEN = os.environ['TELEGRAM_LOGGER_BOT_TOKEN']
TELEGRAM_LOGGER_USER_CHAT_ID = os.environ['TELEGRAM_LOGGER_USER_CHAT_ID']

logger = logging.getLogger(__file__)


class TelegramLogsHandler(logging.Handler):
    def __init__(self, tg_bot, chat_id):
        super().__init__()
        self.chat_id = chat_id
        self.tg_bot = tg_bot

    def emit(self, record):
        log_entry = self.format(record)
        self.tg_bot.send_message(chat_id=self.chat_id, text=log_entry)


def start_command_handler(update, context):
    context.bot.send_message(chat_id=update.effective_chat.id, text='Здравствуйте! Чем можем помочь?')


def answer_handler(update, context):
    try:
        answer = get_answer(update.message.text, update.effective_chat.id, True)
        context.bot.send_message(chat_id=update.effective_chat.id, text=answer)
    except:
        logger.exception('Telegram-бот упал с ошибкой')


def start_bot():
    updater = Updater(token=TELEGRAM_BOT_TOKEN)
    dispatcher = updater.dispatcher
    updater.start_polling()

    start_handler = CommandHandler('start', start_command_handler)
    dispatcher.add_handler(start_handler)

    echo_handler = MessageHandler(Filters.text & (~Filters.command), answer_handler)
    dispatcher.add_handler(echo_handler)


def main():
    logger_bot = telegram.Bot(token=TELEGRAM_LOGGER_BOT_TOKEN)
    logger.setLevel(logging.WARNING)
    logger.addHandler(TelegramLogsHandler(logger_bot, TELEGRAM_LOGGER_USER_CHAT_ID))

    try:
        start_bot()
        logger.warning('Telegram-бот запущен')
    except:
        logger.exception('Telegram-бот упал с ошибкой')


if __name__ == '__main__':
    main()
