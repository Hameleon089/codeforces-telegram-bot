import os
from dotenv import load_dotenv, find_dotenv

if not find_dotenv():
    exit('Переменные окружения не загружены т.к отсутствует файл .env')
else:
    load_dotenv()

# Переменные окружения
BOT_TOKEN = os.getenv('BOT_TOKEN')

DB_NAME = os.getenv('DB_NAME')
DB_USER = os.getenv('DB_USER')
DB_PASSWORD = os.getenv('DB_PASSWORD')
DB_HOST = os.getenv('DB_HOST')

# Перечень команд бота
DEFAULT_COMMANDS = (
    ('start', 'Запустить бота'),
    ('help', 'Вывести справку'),
    ('newcontest', 'Создать новую подборку задач'),
    ('findtask', 'Найти задачу по номеру'),
    ('findcontest', 'Найти контест по номеру')
)

# Константы
MAIN_URL = 'https://codeforces.com'
URL = 'https://codeforces.com/problemset?order=BY_SOLVED_DESC&locale=ru'
DELAY = 3600  # Задержка между парсингом сайта
TASKS_LIMIT = 10  # Максимальное количество задач в контексте
