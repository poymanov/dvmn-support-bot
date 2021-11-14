import os
import json
from dialog_flow import create_intent
from google.api_core.exceptions import GoogleAPIError

LEARNING_DATA_INTENTS_FILE = os.environ['LEARNING_DATA_INTENTS_FILE']


def main():
    try:
        with open(LEARNING_DATA_INTENTS_FILE, "r") as file:
            intents = json.load(file)

    except OSError:
        print('Ошибка открытия файла с вопросами')
        return

    for intent, data in intents.items():
        try:
            create_intent(intent, data['questions'], [data['answer']])
        except GoogleAPIError:
            print('Ошибка создания: {}'.format(intent))


if __name__ == '__main__':
    main()
