import requests
from bs4 import BeautifulSoup as bs

headers = {'accept': '*/*', 'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:70.0) Gecko/20100101 Firefox/70.0'}

base_url = 'https://hh.ru/search/vacancy?area=1&search_period=3&text=python&page=0'

def hh_parse(base_url, headers):
    session = requests.Session()
    request = session.get(base_url, headers=headers)
    if request.status_code == 200:
        print('OK')
    else:
        print('ERROR')

hh_parse(base_url, headers)