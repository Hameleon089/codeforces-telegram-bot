from loguru import logger
from telebot.handler_backends import State, StatesGroup
from telebot.types import Message

from database.database import get_task
from loader import bot
from logs.loggers import func_logger
from utils.task_info import get_task_info


class FindTaskState(StatesGroup):
    """Класс состояний команды findtask"""

    number = State()


@bot.message_handler(commands=['findtask'])
@func_logger
def ask_task_number(message: Message) -> None:
    """
    Message handler. Запрашивает номер задачи

    Args:
        message: сообщение
    """
    user_id = message.from_user.id
    chat_id = message.chat.id
    logger.info(f'Команда = findtask; user_id = {user_id}; chat_id = {chat_id}')

    bot.set_state(user_id, FindTaskState.number, chat_id)
    bot.send_message(user_id, 'Введите номер задачи')


@bot.message_handler(state=FindTaskState.number)
@func_logger
def find_task_result(message: Message) -> None:
    """
    Message handler. Отправляет информацию по задаче

    Args:
        message: сообщение
    """

    user_id = message.from_user.id
    chat_id = message.chat.id

    task = get_task(message.text.upper())

    if task is None:
        text = 'С указанным номером задачу найти не удалось'
    else:
        text = get_task_info(task)
    bot.send_message(user_id, text)

    bot.set_state(user_id, None, chat_id)
