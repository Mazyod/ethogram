
import logging
from ethogram.config import Config
from ethogram.bot import Bot
from ethogram.scheduler import Scheduler
from telegram.ext import Updater


def main():
    logFormat = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    logging.basicConfig(level=logging.INFO, format=logFormat)

    bot = Bot()
    scheduler = Scheduler(4 * 60, bot.update)

    updater = Updater(Config.telegram_token())
    [updater.dispatcher.add_handler(c) for c in bot.commands]

    scheduler.start()

    updater.start_polling()
    updater.idle()


if __name__ == '__main__':
    main()
