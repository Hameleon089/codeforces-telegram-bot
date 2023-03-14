import time

import requests
from bs4 import BeautifulSoup as bs
from loguru import logger

from database.database import insert_to_db
from config.config import DELAY, MAIN_URL, URL


def parse_site(url: str, main_url: str) -> None:
    """
    Парсит информацию с сайта и сохраняет ее в базе данных

    Args:
        url (str): адрес страницы
        main_url (str): адрес сайта
    """

    response = requests.get(url, timeout=10)
    if response.status_code != 200:
        return

    soup = bs(response.text, "html.parser")
    table = soup.find('table', class_='problems')
    rows = table.find_all('tr')
    tasks_list = list()
    for i, row in enumerate(rows):
        if i == 0:
            continue

        td_set = row.find_all('td')
        number = td_set[0].a.string.strip()

        link = ''.join((main_url, td_set[0].a.get('href')))

        divs = td_set[1].find_all('div')
        name = divs[0].a.contents[0].strip()
        links = divs[1].find_all('a')

        topics = list()
        for i_link in links:
            topics.append(i_link.string.strip())

        if td_set[3].span:
            complexity = int(td_set[3].span.string.strip())
        else:
            complexity = 0

        if td_set[4].a:
            solutions_amt = int(td_set[4].a.contents[1].strip()[1:])
        else:
            solutions_amt = 0

        tasks_list.append(
            {
                'name': name,
                'number': number,
                'link': link,
                'complexity': complexity,
                'solutions_amt': solutions_amt,
                'topics': topics
            }
        )

    insert_to_db(tasks_list)

    logger.info(f'Завершен парсинг страницы: {url}')

    pagination = soup.find('div', class_='pagination')
    next_page = pagination.ul.contents[-2]
    if next_page.name == 'li':
        next_page = ''.join((main_url, next_page.a.get('href'), '&locale=ru'))
        parse_site(next_page, main_url)


def infinity_parse() -> None:
    """
    Бесконечно парсит сайт с заданной периодичностью

    Args:
        url (str): адрес страницы
        main_url (str): адрес сайта
        delay (int): задержка в секундах
    """
    while True:
        logger.debug('Начался парсинг сайта')
        parse_site(URL, MAIN_URL)
        logger.debug('Парсинг сайта завершен')
        time.sleep(DELAY)
