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
    # jobs = []
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
        # в каждом div мы будем находить
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
                # try:
                #     data = datetime.strftime('%Y-%m-%d')
                # except ValueError:
                #     data = datetime.now()
                text1 = div.find('div', attrs={'data-qa': 'vacancy-serp__vacancy_snippet_responsibility'}).text.strip()
                text2 = div.find('div', attrs={'data-qa': 'vacancy-serp__vacancy_snippet_requirement'}).text.strip()
                content = text1 + ' ' + text2
                # jobs.append({
                #     'title': title,
                #     'href': href,
                #     'company': company,
                #     'price': price,
                #     'data': data,
                #     'content': content
                # })
            except:
                pass
            save_vacancy(title, href, company, price, data, content)
    #     print(len(jobs))
    # else:
    #     print('ERROR or Done' + str(request.status_code))
    # return jobs

def save_vacancy(title, href, company, price, data, content):
    vacancy_exists = Vacancy.query.filter(Vacancy.href == href).count()
    if not vacancy_exists:
        new_vacancy = Vacancy(title=title, href=href, company=company, price=price, data=data, content=content)
        db.session.add(new_vacancy)
        db.session.commit()



# from datetime import datetime

# RU_MONTH_VALUES = {
#     'января': 1,
#     'февраля': 2,
#     'марта': 3,
#     'апреля': 4,
#     'мая': 5,
#     'июня': 6,
#     'июля': 7,
#     'августа': 8,
#     'сентября': 9,
#     'октября': 10,
#     'ноября': 11,
#     'декабря': 12,
# }

# def int_value_from_ru_month(date_str):
#     return RU_MONTH_VALUES.get(date_str)

# data = "31 октября"
# print(data.split())
# day, month = data.split()
# print(datetime(year=datetime.now().year, month=int_value_from_ru_month(month), day=int(day)))









# from flask import Flask, render_template, Response
# from webapp.model import db, Vacancy

# def create_app():
#     app = Flask(__name__)
#     app.config.from_pyfile('config.py')
#     db.init_app(app)

#     @app.route("/")
#     def index():
#         title = app.config['TITLE']

#         vacancies_list = Vacancy.query.order_by(Vacancy.data.desc()).all()
#         return render_template('index.html', page_title=title, vacancies_list=vacancies_list)

#     @app.route("/update")
#     def update():
#         headers = app.config['HEADERS']
#         base_url =  app.config['BASE_URL']
#         hh_parse(base_url, headers)
#         return Response(status=200)


#     return app