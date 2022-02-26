import requests
import json
import re
from bs4 import BeautifulSoup

headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/98.0.4758.102 Safari/537.36 Edg/98.0.1108.56'}
base_url = 'https://hh.ru'
url = 'https://hh.ru'

vacancy_list = []

while True:
    response = requests.get(url + '/search/vacancy', headers=headers)
    if response.ok:
        dom = BeautifulSoup(response.text, 'html.parser')
        vacancies = dom.find_all('div', {'class': 'vacancy-serp-item_redesigned'})

        for vacancy in vacancies:
            vacancy_text = vacancy.find('a').getText()
            vacancy_data = {}

            salary = vacancy.find('span', {'data-qa': 'vacancy-serp__vacancy-compensation'})
            try:
                salary_str = salary.getText()
                salary_list = salary_str.split(' ')
                regex = r'[\D+\\.]?$'
                if re.search(regex, salary_str):
                    salary_currency = salary_list[-1]
                else:
                    salary_currency = None
                if salary_str.startswith('от'):
                    min_salary = salary_list[1].replace('\u202f', ' ')
                    max_salary = None
                elif salary_str.startswith('до'):
                    min_salary = None
                    max_salary = salary_list[1].replace('\u202f', ' ')
                else:
                    min_salary = salary_list[0].replace('\u202f', ' ')
                    max_salary = salary_list[2].replace('\u202f', ' ')
            except Exception:
                min_salary = None
                max_salary = None
                salary_currency = None

            vacancy_data['vacancy'] = vacancy_text
            vacancy_data['min_salary'] = min_salary
            vacancy_data['max_salary'] = max_salary
            vacancy_data['currency'] = salary_currency
            vacancy_data['source_site'] = base_url
            vacancy_list.append(vacancy_data)

    with open('hh.json', 'w') as file:
        json.dump(vacancies, file, indent=2, ensure_ascii=False)