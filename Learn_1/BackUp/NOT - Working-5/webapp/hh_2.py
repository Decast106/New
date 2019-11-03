import requests
import csv
from bs4 import BeautifulSoup as bs
from datetime import datetime

from webapp.model import db, Vacancy
# from config import HEADERS, BASE_URL
# from flask import Flask

# def create_app():
    # app = Flask(__name__)
    # app.config.from_pyfile('config.py')
    # db.init_app(app)
    # return app

headers = {'accept': '*/*', 'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:70.0) Gecko/20100101 Firefox/70.0'}
base_url = 'https://hh.ru/search/vacancy?area=1&search_period=3&text=Junior+Python+Developer&page=0'

def hh_parse(base_url, headers):
    # app = create_app()
    jobs = []
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
        except Exception as e:
            print(str(e))
            
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
                try:
                    data = datetime.strptime(data, "%Y-%m-%d")
                except(ValueError):
                    data = datetime.now()    
                try:
                    text1 = div.find('div', attrs={'data-qa': 'vacancy-serp__vacancy_snippet_responsibility'}).text.strip()
                except:
                    text1 = ' '
                try:
                    text2 = div.find('div', attrs={'data-qa': 'vacancy-serp__vacancy_snippet_requirement'}).text.strip()
                except:
                    text2 = ' '
                content = text1 + ' ' + text2
                # jobs.append({
                #     'title': title,
                #     'href': href,
                #     'company': company,
                #     'price': price,
                #     'data': data,
                #     'content': content
                # })
                save_vacancy(title, href, company, price, data, content)
            except Exception as e:
                print(str(e))
            
    #     print(len(jobs))
    # else:
    #     print('ERROR or Done' + str(request.status_code))
    # return jobs

def save_vacancy(title, href, company, price, data, content):
    vacancy_exists = Vacancy.query.filter(Vacancy.company == company).count()
    if not vacancy_exists:
        new_vacancy = Vacancy(title=title, href=href, company=company, price=price, data=data, content=content)
        db.session.add(new_vacancy)
        db.session.commit()

# if __name__ == "__main__":
#     hh_parse(BASE_URL, HEADERS)
    