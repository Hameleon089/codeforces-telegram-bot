from loguru import logger
from telebot.handler_backends import State, StatesGroup
from telebot.types import Message

from database.database import get_contest
from loader import bot
from logs.loggers import func_logger
from utils.contest_info import get_contest_info


class FindContestState(StatesGroup):
    """Класс состояний команды findcontest"""

    number = State()


@bot.message_handler(commands=['findcontest'])
@func_logger
def ask_contest_number(message: Message) -> None:
    """
    Message handler. Запрашивает номер контеста

    Args:
        message: сообщение
    """
    user_id = message.from_user.id
    chat_id = message.chat.id
    logger.info(f'Команда = findcontest; user_id = {user_id}; chat_id = {chat_id}')

    bot.set_state(user_id, FindContestState.number, chat_id)
    bot.send_message(user_id, 'Введите номер контеста')


@bot.message_handler(state=FindContestState.number)
@func_logger
def find_contest_result(message: Message) -> None:
    """
    Message handler. Проверяет номер и отправляет информацию по контесту

    Args:
        message: сообщение
    """

    user_id = message.from_user.id
    chat_id = message.chat.id

    if not message.text.isdigit():
        text = 'Номер контеста должен быть числом\nПовторите ввод'
    else:
        contest = get_contest(int(message.text))

        if contest is None:
            text = 'С указанным номером контест найти не удалось'
        else:
            text = get_contest_info(contest.tasks, contest)
        bot.set_state(user_id, None, chat_id)

    bot.send_message(user_id, text)