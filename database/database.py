from typing import List, Optional

from peewee import (CharField, ForeignKeyField, IntegerField, Model,
                    PostgresqlDatabase, SqliteDatabase)

from config.config import DB_HOST, DB_NAME, DB_PASSWORD, DB_USER
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
    """Класс Контест"""


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


@func_logger
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
def create_contest(topic: str, complexity: int) -> List[Task]:
    """
    Создает подборку из 10 задач с заданной сложностью и темой

    Args:
        topic: тема
        complexity: сложность

    :return: список (подборка) задач
    """

    with db.atomic():
        contest = Contest.create()
        tasks_list = Task.select().join(TaskTopic).join(Topic).where(
            Topic.name == topic, Task.complexity == complexity, Task.contest == None
        ).limit(10)
        for task in tasks_list:
            task.contest = contest
            task.save()

    return tasks_list


@func_logger
def get_task(number: str) -> Optional[Task]:
    """
    Возвращает задачу из БД по номеру

    :return: задача, если искомой задачи нет - None
    """

    with db.atomic():
        task = Task.get_or_none(number=number)
    return task
