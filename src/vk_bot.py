import os
import logging
import random
import vk_api as vk
from vk_api.longpoll import VkLongPoll, VkEventType
from dialog_flow import get_answer
from tg_logger import set_logger

VK_GROUP_TOKEN = os.environ['VK_GROUP_TOKEN']

logger = logging.getLogger(__file__)


def answer_handler(event, vk_api):
    answer = get_answer(event.text, 'vk-{}'.format(event.user_id), False)

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
    set_logger(logger)

    try:
        logger.warning('Бот группы ВК запущен')
        start_bot()
    except:
        logger.exception('Бот группы ВК упал с ошибкой')


if __name__ == '__main__':
    main()
