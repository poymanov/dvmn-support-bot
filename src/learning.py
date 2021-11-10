import os
import json
from google.cloud import dialogflow

DIALOG_FLOW_PROJECT_ID = os.environ['DIALOG_FLOW_PROJECT_ID']
LEARNING_DATA_INTENTS_FILE = os.environ['LEARNING_DATA_INTENTS_FILE']


def create_intent(display_name, training_phrases_parts, message_texts):
    intents_client = dialogflow.IntentsClient()

    parent = dialogflow.AgentsClient.agent_path(DIALOG_FLOW_PROJECT_ID)
    training_phrases = []

    for training_phrases_part in training_phrases_parts:
        part = dialogflow.Intent.TrainingPhrase.Part(text=training_phrases_part)
        training_phrase = dialogflow.Intent.TrainingPhrase(parts=[part])
        training_phrases.append(training_phrase)

    text = dialogflow.Intent.Message.Text(text=message_texts)
    message = dialogflow.Intent.Message(text=text)

    intent = dialogflow.Intent(
        display_name=display_name, training_phrases=training_phrases, messages=[message]
    )

    intents_client.create_intent(request={"parent": parent, "intent": intent})

    print('Создано: {}'.format(display_name))


def main():
    try:
        with open(LEARNING_DATA_INTENTS_FILE, "r") as file:
            intents = json.load(file)

    except:
        print('Ошибка открытия файла с вопросами')
        return

    for intent, data in intents.items():
        try:
            create_intent(intent, data['questions'], [data['answer']])
        except:
            print('Ошибка создания: {}'.format(intent))


if __name__ == '__main__':
    main()
