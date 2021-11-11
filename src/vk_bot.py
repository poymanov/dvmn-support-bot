import os
import logging
import random
import vk_api as vk
import telegram
from vk_api.longpoll import VkLongPoll, VkEventType
from dialog_flow import get_answer

VK_GROUP_TOKEN = os.environ['VK_GROUP_TOKEN']
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


def answer_handler(event, vk_api):
    answer = get_answer(event.text, event.user_id, False)

    if answer is not None:
        vk_api.messages.send(
            user_id=event.user_id,
            message=answer,
            random_id=random.randint(1, 1000)
        )


def start_bot():
    vk_session = vk.VkApi(token=VK_GROUP_TOKEN)

    vk_api = vk_session.get_api()
    longpoll = VkLongPoll(vk_session)
    for event in longpoll.listen():
        if event.type == VkEventType.MESSAGE_NEW and event.to_me:
            answer_handler(event, vk_api)


def main():
    logger_bot = telegram.Bot(token=TELEGRAM_LOGGER_BOT_TOKEN)
    logger.setLevel(logging.WARNING)
    logger.addHandler(TelegramLogsHandler(logger_bot, TELEGRAM_LOGGER_USER_CHAT_ID))

    try:
        logger.warning('Бот группы ВК запущен')
        start_bot()
    except:
        logger.exception('Бот группы ВК упал с ошибкой')


if __name__ == '__main__':
    main()
