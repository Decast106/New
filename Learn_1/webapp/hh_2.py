from datetime import datetime
import requests
import csv
from bs4 import BeautifulSoup as bs

from webapp.model import db, Vacancy

RU_MONTH_VALUES = {
    'января': 1,
    'февраля': 2,
    'марта': 3,
    'апреля': 4,
    'мая': 5,
    'июня': 6,
    'июля': 7,
    'августа': 8,
    'сентября': 9,
    'октября': 10,
    'ноября': 11,
    'декабря': 12,
}

headers = {'accept': '*/*', 'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:70.0) Gecko/20100101 Firefox/70.0'}

base_url = 'https://hh.ru/search/vacancy?area=1&search_period=3&text=Junior+Python+Developer&page=0'

def int_value_from_ru_month(date_str):
    return RU_MONTH_VALUES.get(date_str)

def hh_parse(base_url, headers):
    urls = []
    urls.append(base_url)
    session = requests.Session()
    request = session.get(base_url, headers=headers)
    if request.status_code == 200:
        request = session.get(base_url, headers=headers)
        soup = bs(request.content, 'lxml')
        try:
            pagination = soup.find_all('a', attrs={'data-qa': 'pager-page'})
            count = int(pagination[-1].text)
            for i in range(count):
                url = f'https://hh.ru/search/vacancy?area=1&search_period=3&text=Junior+Python+Developer&page={i}'
                if url not in urls:
                    urls.append(url)
        except:
            pass
    for url in urls:
        request = session.get(url, headers=headers)
        soup = bs(request.content, 'lxml')
        divs = soup.find_all('div', attrs={'class': 'vacancy-serp-item'})
        for div in divs:
            try:
                title = div.find('a', attrs={'data-qa': 'vacancy-serp__vacancy-title'}).text
                href = div.find('a', attrs={'data-qa': 'vacancy-serp__vacancy-title'})['href']
                try:
                    company = div.find('a', attrs={'data-qa': 'vacancy-serp__vacancy-employer'}).text
                except:
                    company = ' '
                try:
                    price = div.find('div', attrs={'data-qa': 'vacancy-serp__vacancy-compensation'}).text.strip()
                except:
                    price = ' '
                data = div.find('span', attrs={'data-qa': 'vacancy-serp__vacancy-date'}).text.strip() 
                day, month = data.split()
                data = datetime(year=datetime.now().year, month=int_value_from_ru_month(month), day=int(day))
                try:
                    data = datetime(year=datetime.now().year, month=int_value_from_ru_month(month), day=int(day))
                except(ValueError):
                    data = datetime.now()
                text1 = div.find('div', attrs={'data-qa': 'vacancy-serp__vacancy_snippet_responsibility'}).text.strip()
                text2 = div.find('div', attrs={'data-qa': 'vacancy-serp__vacancy_snippet_requirement'}).text.strip()
                content = text1 + ' ' + text2
            except:
                pass
            save_vacancy(title, href, company, price, data, content)

def save_vacancy(title, href, company, price, data, content):
    vacancy_exists = Vacancy.query.filter(Vacancy.href == href).count()
    if not vacancy_exists:
        new_vacancy = Vacancy(title=title, href=href, company=company, price=price, data=data, content=content)
        db.session.add(new_vacancy)
        db.session.commit()
