
import logging
from ethogram.config import Config
from ethogram.bot import Bot
from ethogram.scheduler import Scheduler
from telegram.ext import Updater


def main():
    logFormat = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    logging.basicConfig(level=logging.INFO, format=logFormat)

    config = Config()
    bot = Bot()
    scheduler = Scheduler(4 * 60, bot.update)

    updater = Updater(config.telegram_token)
    [updater.dispatcher.add_handler(c) for c in bot.commands]

    scheduler.start()

    # TODO - configurable filepaths and listen domain
    cert_file = "certs/ca.crt"
    pkey_file = "certs/ca.key"
    updater.start_webhook(listen='0.0.0.0',
                          port=config.webhook_port,
                          url_path=config.telegram_token,
                          key=pkey_file,
                          cert=cert_file,
                          webhook_url=f'https://{config.webhook_host}:{config.webhook_port}/{config.telegram_token}')
    updater.idle()


if __name__ == '__main__':
    main()
