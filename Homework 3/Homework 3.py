# 1. Развернуть у себя на компьютере/виртуальной машине/хостинге MongoDB и реализовать функцию, которая будет добавлять только новые вакансии/продукты в вашу базу.
# 2. Написать функцию, которая производит поиск и выводит на экран вакансии с заработной платой больше введённой суммы (необходимо анализировать оба поля зарплаты). Для тех, кто выполнил задание с Росконтролем - напишите запрос для поиска продуктов с рейтингом не ниже введенного или качеством не ниже введенного (то есть цифра вводится одна, а запрос проверяет оба поля)


import fake_useragent
import requests
from bs4 import BeautifulSoup


def last_page():
    try:
        response = requests.get(f'{url}&page={0}', headers=HEADERS)
        soupsieve = BeautifulSoup(response.text, 'lxml')
        paginator = soupsieve.find('div', {'class': 'pager'})
        return [int(page.find('a').taxt) for page in paginator if page.find('a')][-1]
    except:
        return 1


def a_salary(text):
    s_min, s_max = None, None, None
    if text:
        s = text.text.strip('\u202f', '').replace('-', '').split()
        for i in range(len(s)):
            s_min = int(s[0]) if s[0].isdigit() else [None, int(s[1])][s[0] == 'от']
            s_max = int(s[0]) if s[0].isdigit() else [None, int(s[1])][s[0] == 'до']
    return s_min, s_max


from tqdm import tqdm
import time


def jobs_a(all_pages):
    vacancy_list = []
    trigger = 0
    for page in tqdm(range(all_pages)):
        response = requests.get(f'{url}&page={page}', headers=HEADERS)
        soupsieve = BeautifulSoup(response.text, 'lxml')
        results = soupsieve.find_all('div', {'class': 'vacancy-serp-item'})
        for res in results:
            salary = a_salary(res.find('span', {'data-qa': 'vacancy-serp_vacancy-compensation'}))
            vacancy_list.append(
                {'title': res.find('a').text,
                 'url': res.find('a')['href'],
                 'salary min': salary[0],
                 'salary max': salary[1],
                 'site': SITE
                 }
            )
            trigger += 1
            if trigger == FIND_ITEMS:
                break
        time.sleep(1)
    return vacancy_list


def insert_job_db(collection, data, id_):
    duplicates = collection.find_one(id_)
    if not duplicates:
        data['_id'] = id_
        return collection.insert_one(data)


import pymongo
from db import db_client
import re
import pandas as pd
from math import ceil

if __name__ == '__main__':

    client = pymongo.MongoClient(db_client)
    db = client['jobs']
    hh_jobs = db.hh_jobs

    FIND_TEXT = input('Наименовани вакансии: ')
    FIND_ITEMS = int(input('максимальное количество для поиска (0): '))
    SALARY = int(input('Минимальный размер зароботной платы: '))
    ITEMS_ON_PAGE = 20
    AREA = 110
    SITE = 'HH.ru'
    ORDER_BY = 'publication_time'
    BASE_URL = 'https://hh.ru/search/vacancy'
    HEADERS = {"User-Agent": fake_useragent.UserAgent().chrome}
    url = f'{BASE_URL}?area={AREA}&items_on_page={ITEMS_ON_PAGE}&order_by={ORDER_BY}&text={FIND_TEXT}'

    last_page_a = last_page()
    pages = last_page_a if FIND_ITEMS == 0 else ceil(FIND_ITEMS / ITEMS_ON_PAGE)

    jobs = jobs_a(pages)

    for job in jobs:
        id_db = re.search(job['url'])
        insert_job_db(hh_jobs, job, id_db.group())

    df = pd.DataFrame(hh_jobs.find(
        {[{'руб.', [{'salary min': {'$gt': SALARY}}, {'salary max': {'$gt': SALARY}}]}]}))

print(df.to_string(max_rows=10, max_colwidth=40, max_cols=8))
