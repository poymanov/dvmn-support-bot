import os
import logging
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
from dialog_flow import get_answer

TELEGRAM_BOT_TOKEN = os.environ['TELEGRAM_BOT_TOKEN']


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
