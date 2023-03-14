from typing import List, Optional

from peewee import (CharField, ForeignKeyField, IntegerField, Model,
                    PostgresqlDatabase, SqliteDatabase)

from config.config import DB_HOST, DB_NAME, DB_PASSWORD, DB_USER, TASKS_LIMIT
from logs.loggers import func_logger

# db = PostgresqlDatabase(
#     DB_NAME,
#     user=DB_USER,
#     password=DB_PASSWORD,
#     host=DB_HOST
# )

db = SqliteDatabase('data.db')


class BaseModel(Model):
    """Класс базовой модели ORM"""

    class Meta:
        # database: PostgresqlDatabase = db
        database: SqliteDatabase = db


class Contest(BaseModel):
    """
    Класс Контест

    Attributes:
        complexity: сложность задач
        topic: тема задач
    """
    complexity = IntegerField()
    topic = CharField()


class Task(BaseModel):
    """
    Класс Задача

    Attributes:
        number: номер
        name: название
        link: ссылка
        complexity: сложность
        solutions_amt: количество решений
        contest: контест
    """

    number = CharField(unique=True)
    name = CharField()
    link = CharField()
    complexity = IntegerField()
    solutions_amt = IntegerField()
    contest = ForeignKeyField(Contest, null=True, backref='tasks')


class Topic(BaseModel):
    """
    Класс Тема

    Attributes:
        name: название
    """

    name = CharField(unique=True)


class TaskTopic(BaseModel):
    """
    Класс тема задачи

    Attributes:
        task: задача
        topic: тема
    """

    task = ForeignKeyField(Task, backref='task_topics')
    topic = ForeignKeyField(Topic, backref='topic_tasks')


@func_logger
def create_tables():
    """Создает таблицы в базе данных"""

    with db:
        db.create_tables([Contest, Task, Topic, TaskTopic])


def add_topics(topics: List[str], task: Task) -> None:
    """
    Добавляет темы для задачи

    Args:
        topics: список тем
        task: задача
    """

    for topic_name in topics:
        topic, _ = Topic.get_or_create(name=topic_name)
        TaskTopic.create(task=task, topic=topic)


@func_logger
def insert_to_db(tasks_list: List[dict]) -> None:
    """
    Сохраняет список задач в базе данных

    Args:
        tasks_list: список задач
    """

    with db.atomic():
        for task in tasks_list:
            db_task = Task.get_or_none(number=task['number'])
            if db_task is None:
                db_task = Task.create(
                    number=task['number'],
                    name=task['name'],
                    link=task['link'],
                    complexity=task['complexity'],
                    solutions_amt = task['solutions_amt']
                )

                add_topics(task['topics'], db_task)
            elif (
                db_task.complexity != task['complexity'] or
                db_task.solutions_amt != task['solutions_amt']
            ):
                db_task.complexity = task['complexity']
                db_task.solutions_amt = task['solutions_amt']
                db_task.save()


@func_logger
def create_contest(topic: str, complexity: int) -> tuple:
    """
    Создает подборку из 10 задач с заданной сложностью и темой

    Args:
        topic: тема
        complexity: сложность

    Returns: номер контеста и список (подборка) задач
    """

    with db.atomic():
        tasks_list = Task.select().join(TaskTopic).join(Topic).where(
            Topic.name == topic, Task.complexity == complexity, Task.contest == None
        ).limit(TASKS_LIMIT)

        if not tasks_list:
            return None, tasks_list

        contest = Contest.create(topic=topic, complexity=complexity)
        for task in tasks_list:
            task.contest = contest
            task.save()

    return contest, tasks_list


@func_logger
def get_task(number: str) -> Optional[Task]:
    """
    Возвращает задачу из БД по номеру

    Returns: задача, если искомой задачи нет - None
    """

    task = Task.get_or_none(number=number)
    return task


@func_logger
def get_topics(task: Task) -> List[str]:
    """
    Возвращает список тем для задачи

    Args:
        task: задача

    Returns: список тем
    """

    topics = Topic.select().join(TaskTopic).where(TaskTopic.task == task)
    topics_name = list()
    for topic in topics:
        topics_name.append(topic.name)

    return topics_name


@func_logger
def get_contest(num: int) -> Optional[Contest]:
    """
    Возвращает контест из БД по номеру

    Args:
        num: номер контеста

    Returns: контест
    """

    contest = Contest.get_or_none(id=num)
    return contest
