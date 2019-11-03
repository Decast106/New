import os
basedir = os.path.abspath(os.path.dirname(__file__))

TITLE = 'Вакансии Junior Python Developer за три дня - парсинг с HH.ru'
HEADERS = {'accept': '*/*', 'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:70.0) Gecko/20100101 Firefox/70.0'}
BASE_URL = 'https://hh.ru/search/vacancy?area=1&search_period=3&text=Junior+Python+Developer&page=0'

SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, '..', 'webapp.db')


