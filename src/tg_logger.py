import logging
import telegram
import os

TELEGRAM_LOGGER_BOT_TOKEN = os.environ['TELEGRAM_LOGGER_BOT_TOKEN']
TELEGRAM_LOGGER_USER_CHAT_ID = os.environ['TELEGRAM_LOGGER_USER_CHAT_ID']


class TelegramLogsHandler(logging.Handler):
    def __init__(self, tg_bot, chat_id):
        super().__init__()
        self.chat_id = chat_id
        self.tg_bot = tg_bot

    def emit(self, record):
        log_entry = self.format(record)
        self.tg_bot.send_message(chat_id=self.chat_id, text=log_entry)


def set_logger(logger):
    logger_bot = telegram.Bot(token=TELEGRAM_LOGGER_BOT_TOKEN)
    logger.setLevel(logging.WARNING)
    logger.addHandler(TelegramLogsHandler(logger_bot, TELEGRAM_LOGGER_USER_CHAT_ID))
