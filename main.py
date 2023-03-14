import os
from threading import Thread

from loguru import logger
from telebot.custom_filters import StateFilter

import handlers
from database.database import create_tables
from loader import bot
from utils.parser import infinity_parse
from utils.set_bot_commands import set_default_commands

if __name__ == '__main__':
    logger.add(os.path.join('logs', 'logs.log'),
            format='{time} {level} {message}',
            retention='2 days')
    logger.debug('#### Запущен новый сеанс ####')

    create_tables()

    bot.add_custom_filter(StateFilter(bot))
    set_default_commands(bot)

    stream_1 = Thread(target=infinity_parse)
#     stream_1.start()
    stream_2 = Thread(target=bot.infinity_polling)
    stream_2.start()
