from loguru import logger
from telebot.handler_backends import State, StatesGroup
from telebot.types import Message

from database.database import create_contest
from loader import bot
from logs.loggers import func_logger
from utils.contest_info import get_contest_info


class NewContestState(StatesGroup):
    """Класс состояний команды newcontest"""

    topic = State()
    complexity = State()


@bot.message_handler(commands=['newcontest'])
@func_logger
def ask_task_topic(message: Message) -> None:
    """
    Message handler. Запрашивает тему задач

    Args:
        message: сообщение
    """
    user_id = message.from_user.id
    chat_id = message.chat.id
    logger.info(f'Комманда = newcontest; user_id = {user_id}; chat_id = {chat_id}')

    bot.set_state(user_id, NewContestState.topic, chat_id)
    bot.send_message(user_id, 'Введите тему задач')


@bot.message_handler(state=NewContestState.topic)
@func_logger
def ask_task_complexity(message: Message) -> None:
    """
    Message handler. Запрашивает сложность задач

    Args:
        message: сообщение
    """
    user_id = message.from_user.id
    chat_id = message.chat.id

    with bot.retrieve_data(user_id, chat_id) as data:
        data['topic'] = message.text.lower()

    bot.set_state(user_id, NewContestState.complexity, chat_id)
    bot.send_message(user_id, 'Введите сложность задач')


@bot.message_handler(state=NewContestState.complexity)
@func_logger
def new_contest_result(message: Message) -> None:
    """
    Message handler. Проверяет сложность и отправляет подборку задач

    Args:
        message: сообщение
    """
    user_id = message.from_user.id
    chat_id = message.chat.id

    if not message.text.isdigit() or len(message.text) > 4:
        text = 'Сложность задач должна состоять из цифр (количество символов не более 4)\nПовторите ввод'
    else:
        with bot.retrieve_data(user_id, chat_id) as data:
            contest, tasks_list = create_contest(data['topic'], int(message.text))
        if contest is None:
            text = 'С указанными данными создать подборку задач не удалось'
        else:
            text = get_contest_info(tasks_list, contest)

        bot.set_state(user_id, None, chat_id)

    bot.send_message(user_id, text)
