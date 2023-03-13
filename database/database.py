from typing import List

from peewee import PostgresqlDatabase, Model, CharField, IntegerField, ForeignKeyField, SqliteDatabase
from config.config import DB_NAME, DB_USER, DB_PASSWORD, DB_HOST

# db = PostgresqlDatabase(
#     DB_NAME,
#     user=DB_USER,
#     password=DB_PASSWORD,
#     host=DB_HOST   
# )

db = SqliteDatabase('data.db')


class BaseModel(Model):
    """Класс базовой модели"""
    
    class Meta:
        # database: PostgresqlDatabase = db
        database: SqliteDatabase = db


class Contest(BaseModel):
    """Класс Контест"""

        
class Task(BaseModel):
    """Класс Задача"""
    
    number = CharField(unique=True)
    name = CharField()
    link = CharField()
    complexity = IntegerField()
    solutions_amt = IntegerField()
    contest = ForeignKeyField(Contest, null=True, backref='tasks')
   
    
class Topic(BaseModel):
    """Класс Тема"""
    
    name = CharField(unique=True)
    

class TaskTopic(BaseModel):
    """Класс тема задачи"""
    
    task = ForeignKeyField(Task, backref='task_topics')
    topic = ForeignKeyField(Topic, backref='topic_tasks')


def create_tables():
    """Создает таблицы в базе данных"""

    with db:
        db.create_tables([Contest, Task, Topic, TaskTopic])
    

def add_topics(topics: List[str], task: Task) -> None:
    """Добавляет темы для задачи

    Args:
        topics (List[str]): список тем
        task (Task): задача
    """
    
    for topic_name in topics:
        topic, _ = Topic.get_or_create(name=topic_name)
        TaskTopic.create(task=task, topic=topic)   
    

def insert_to_db(tasks_list: List[dict]) -> None:
    """
    Сохраняет список задач в базе данных
    
    Args:
        tasks_list (List[dict]): список задач
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
