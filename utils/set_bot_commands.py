from telebot.types import BotCommand
from telebot import TeleBot

from config.config import DEFAULT_COMMANDS
from logs.loggers import func_logger


@func_logger
def set_default_commands(bot: TeleBot) -> None:
    """
    Устанавливает команды для бота

    Args:
        bot: бот
    """

    bot.set_my_commands(
        [BotCommand(*i) for i in DEFAULT_COMMANDS]
    )
