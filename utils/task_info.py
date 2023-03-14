from database.database import Task, get_topics


def get_task_info(task: Task, full=True) -> str:
    """
    Возвращает строку с информацией о задаче

    Args:
        task: задача
        full: флаг вывода полной информации по задаче

    Returns: строка с информацией о задаче
    """

    info = '\n'.join((
        f'Номер: {task.number}',
        f'Название: {task.name}',
        f'Количество решений: {task.solutions_amt}',
        f'Темы: {", ".join(get_topics(task))}',
    ))

    if full:
        contest = task.contest.id if task.contest else 'нет'
        info = '\n'.join((
            info,
            f'Сложность: {task.complexity}',
            f'Контест: {contest}',
        ))

    return '\n'.join((info, f'Ссылка: {task.link}'))