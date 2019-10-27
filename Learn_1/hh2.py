import requests

from bs4 import BeautifulSoup as bs

import csv



headers = {'accept': '*/*',

           'user-agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.102 Safari/537.36'}



base_url = 'https://belgorod.hh.ru/search/vacancy?area=1817&clusters=true&enable_snippets=true&no_magic=true&search_field=name&search_field=description&text=python&page=0'



def hh_parse(base_url, headers):

    jobs = []

    urls = [] # создаем список для всех страниц

    urls.append(base_url) # вносим в список первую (базовую) страницу

    session = requests.Session() #создаем сессию, будто зашел один пользователь и просматривает вакансии

    request = session.get(base_url, headers= headers) #Эмулируем открытие страницы в браузере

    if request.status_code == 200: #проверяем, что сервер передал нам данные

        soup = bs(request.content, 'html.parser') # считали весь html со страницы в base_url



        # попробуем найти элементы пагинации (навигация по номерам страниц) в коде

        try:

            pagination = soup.find_all('a', attrs={'data-qa': 'pager-page'}) # в переменную(ТИП СПИСОК) вкладываем все элементы пагинации

            count_pagination = int(pagination[-1].text) # получаем значение крайнего элемента справа из списка = кол-во страниц

            # добавляем в список те страницы, которых там еще нет (2,3, 4..)

            for i in range(count_pagination):

                url = f'https://belgorod.hh.ru/search/vacancy?area=1817&clusters=true&enable_snippets=true&no_magic=true&search_field=name&search_field=description&text=python&page={i}'

                if url not in urls:

                    urls.append(url)

        except:

            pass # если ни одного элемента не найдено, просто пропускаем ошибку



        for url in urls:

            request = session.get(url, headers= headers) # Эмулируем открытие страницы в браузере

            soup = bs(request.content, 'html.parser') # считали весь html со страницы в base_url

            divs = soup.find_all('div', attrs={'data-qa': 'vacancy-serp__vacancy'})

            for div in divs:

                title = div.find('a', attrs={'data-qa': 'vacancy-serp__vacancy-title'}).text

                href = div.find('a', attrs={'data-qa': 'vacancy-serp__vacancy-title'})['href']

                jobs.append({

                    'title': title,

                    'href': href

                            })



        for i in jobs:

            print(i)



    else:

        print('ERROR')

    return jobs



def files_writer(jobs):

    with open('parserJobs2-1.csv', 'w', newline='') as file:

        a_pen = csv.writer(file)

        a_pen.writerow(('название', 'url'))

        for job in jobs:

            a_pen.writerow((job['title'], job['href']))



jobs = hh_parse(base_url, headers)

files_writer(jobs)