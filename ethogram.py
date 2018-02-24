#!/usr/bin/env python3

from telegram import Bot
from telegram.ext import Updater, CommandHandler
import os
import json
from urllib.request import urlopen


def hello(bot, update):
    update.message.reply_text(
        'Hello {}'.format(update.message.from_user.first_name)
    )

def prepare_message(rig):
    return "{rig_name}: {hashrate} H/s".format(
        rig_name=rig["rack_loc"], hashrate=rig["hash"])

def main():

    token = os.environ["TELEGRAM_TOKEN"]
    chat_id = os.environ["TELEGRAM_GROUP_CHAT_ID"]
    ethos_panel_id = os.environ["ETHOS_PANEL_ID"]
    assert(token and chat_id)

    ethos_response_raw = urlopen("http://%s.ethosdistro.com/?json=yes" % (ethos_panel_id))
    ethos_response = json.loads(ethos_response_raw.read().decode())

    message = []
    for rig in ethos_response["rigs"].values():
        message.append(prepare_message(rig))

    bot = Bot(token)
    bot.send_message(text="\n".join(message), chat_id=chat_id)

    updater = Updater(token)
    updater.dispatcher.add_handler(CommandHandler('hello', hello))
    updater.start_polling()
    updater.idle()


if __name__ == '__main__':
    main()
