import os
from google.cloud import dialogflow

DIALOG_FLOW_PROJECT_ID = os.environ['DIALOG_FLOW_PROJECT_ID']
DIALOG_FLOW_LANGUAGE_CODE = os.environ['DIALOG_FLOW_LANGUAGE_CODE']


def get_answer(input_text, session_id, return_fallback_message):
    session_client = dialogflow.SessionsClient()
    session = session_client.session_path(DIALOG_FLOW_PROJECT_ID, session_id)

    text_input = dialogflow.TextInput(text=input_text, language_code=DIALOG_FLOW_LANGUAGE_CODE)

    query_input = dialogflow.QueryInput(text=text_input)

    response = session_client.detect_intent(
        request={"session": session, "query_input": query_input}
    )

    if response.query_result.intent.is_fallback and not return_fallback_message:
        return None

    return response.query_result.fulfillment_text


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
