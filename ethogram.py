#!/usr/bin/env python3

from telegram.ext import Updater, CommandHandler
import os

def hello(bot, update):
    update.message.reply_text(
        'Hello {}'.format(update.message.from_user.first_name)
    )

def main():

    token = os.environ["TELEGRAM_TOKEN"]
    assert(token)

    updater = Updater(token)
    updater.dispatcher.add_handler(CommandHandler('hello', hello))
    updater.start_polling()
    updater.idle()


if __name__ == '__main__':
    main()
