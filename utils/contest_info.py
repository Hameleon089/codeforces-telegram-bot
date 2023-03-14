from typing import List

from database.database import Contest, Task
from utils.task_info import get_task_info
from logs.loggers import func_logger


@func_logger
def get_contest_info(tasks: List[Task], contest: Contest) -> str:
    """
    Возвращает строку с информацией по задачам из подборки

    Args:
        tasks: подборка задач
        num: номер контеста

    Returns: строка с информацией по задачам
    """
    info = f'Контест №{contest.get_id()}\nТема - {contest.topic}\nСложность - {contest.complexity}\n'
    tasks_info = '\n\n'.join([
        '\n'.join((f'* Задача {i+1}', get_task_info(task, full=False)))
        for i, task in enumerate(tasks)
        ])
    return '\n'.join((info, tasks_info))
