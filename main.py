import os

from loguru import logger
from telebot.custom_filters import StateFilter

import handlers
from config.config import DELAY, MAIN_URL, URL
from database.database import create_contest, create_tables
from loader import bot
from utils.parser import infinity_parser
from utils.set_bot_commands import set_default_commands

if __name__ == '__main__':
    logger.add(os.path.join('logs', 'logs.log'),
            format='{time} {level} {message}',
            retention='2 days')
    logger.debug('#### Запущен новый сеанс ####')

    create_tables()

    # infinity_parser(URL, MAIN_URL, DELAY)

    bot.add_custom_filter(StateFilter(bot))
    set_default_commands(bot)
    bot.infinity_polling()
