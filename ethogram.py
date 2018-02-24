#!/usr/bin/env python3

from telegram import Bot
from telegram.ext import Updater, CommandHandler
import os

def hello(bot, update):
    update.message.reply_text(
        'Hello {}'.format(update.message.from_user.first_name)
    )

def main():

    token = os.environ["TELEGRAM_TOKEN"]
    chat_id = os.environ["TELEGRAM_GROUP_CHAT_ID"]
    assert(token and chat_id)

    bot = Bot(token)
    bot.send_message(text="testing, testing, 123", chat_id=chat_id)

    updater = Updater(token)
    updater.dispatcher.add_handler(CommandHandler('hello', hello))
    updater.start_polling()
    updater.idle()


if __name__ == '__main__':
    main()
