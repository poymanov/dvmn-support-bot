import os
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
import logging
from google.cloud import dialogflow

TELEGRAM_BOT_TOKEN = os.environ['TELEGRAM_BOT_TOKEN']
DIALOG_FLOW_PROJECT_ID = os.environ['DIALOG_FLOW_PROJECT_ID']
DIALOG_FLOW_LANGUAGE_CODE = os.environ['DIALOG_FLOW_LANGUAGE_CODE']


def get_answer(input_text, session_id):
    try:
        session_client = dialogflow.SessionsClient()
        session = session_client.session_path(DIALOG_FLOW_PROJECT_ID, session_id)

        text_input = dialogflow.TextInput(text=input_text, language_code=DIALOG_FLOW_LANGUAGE_CODE)

        query_input = dialogflow.QueryInput(text=text_input)

        response = session_client.detect_intent(
            request={"session": session, "query_input": query_input}
        )

        return response.query_result.fulfillment_text
    except Exception:
        return 'Мы не можем ответить на ваш вопрос'


def start(update, context):
    context.bot.send_message(chat_id=update.effective_chat.id, text="Здравствуйте")


def answer(update, context):
    context.bot.send_message(chat_id=update.effective_chat.id,
                             text=get_answer(update.message.text, update.effective_chat.id))


def main():
    logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)

    updater = Updater(token=TELEGRAM_BOT_TOKEN)
    dispatcher = updater.dispatcher
    updater.start_polling()

    start_handler = CommandHandler('start', start)
    dispatcher.add_handler(start_handler)

    echo_handler = MessageHandler(Filters.text & (~Filters.command), answer)
    dispatcher.add_handler(echo_handler)


if __name__ == '__main__':
    main()
