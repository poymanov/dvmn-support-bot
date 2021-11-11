import os
import random
import vk_api as vk
from vk_api.longpoll import VkLongPoll, VkEventType
from dialog_flow import get_answer

VK_GROUP_TOKEN = os.environ['VK_GROUP_TOKEN']


def answer(event, vk_api):
    answer = get_answer(event.text, event.user_id, False)

    if answer is not None:
        vk_api.messages.send(
            user_id=event.user_id,
            message=answer,
            random_id=random.randint(1, 1000)
        )


def main():
    vk_session = vk.VkApi(token=VK_GROUP_TOKEN)

    vk_api = vk_session.get_api()
    longpoll = VkLongPoll(vk_session)
    for event in longpoll.listen():
        if event.type == VkEventType.MESSAGE_NEW and event.to_me:
            answer(event, vk_api)


if __name__ == '__main__':
    main()
