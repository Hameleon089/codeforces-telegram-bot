from config.config import URL, MAIN_URL
from database.database import create_tables
from utils.parser import parse_site

if __name__ == '__main__':
    create_tables()
    # parse_site(URL, MAIN_URL)


