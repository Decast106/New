import requests
import csv
from bs4 import BeautifulSoup as bs

headers = {'accept': '*/*',
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:70.0) Gecko/20100101 Firefox/70.0'}

base_url = 'https://hh.ru/search/vacancy?area=1&search_period=3&text=Junior+Python+Developer&page=0'

def hh_parse(base_url, headers):
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
                company = div.find('a', attrs={'data-qa': 'vacancy-serp__vacancy-employer'}).text
                try:
                    price = div.find('div', attrs={'data-qa': 'vacancy-serp__vacancy-compensation'}).text.strip()
                except:
                    price = ' '
                data = div.find('span', attrs={'data-qa': 'vacancy-serp__vacancy-date'}).text.strip()     
                text1 = div.find('div', attrs={'data-qa': 'vacancy-serp__vacancy_snippet_responsibility'}).text.strip()
                text2 = div.find('div', attrs={'data-qa': 'vacancy-serp__vacancy_snippet_requirement'}).text.strip()
                content = text1 + ' ' + text2
                jobs.append({
                    'title': title,
                    'href': href,
                    'company': company,
                    'price': price,
                    'data': data,
                    'content': content
                })
            except:
                pass
        print(len(jobs))
    else:
        print('ERROR or Done' + str(request.status_code))
    return jobs

# #  Вывод в файл csv
# def files_writer(jobs):
#     with open('parsed_jobs.cvs', 'w', encoding='utf-8') as file:
#         a_pen = csv.writer(file)
#         a_pen.writerow(('Название вакансии', 'URL', 'Название компании', 'Описание'))
#         for job in jobs:
#             a_pen.writerow((job['title'], job['href'], job['company'], job['content']))
# jobs = hh_parse(base_url, headers)
# files_writer(jobs)


# def get_html(url):
#     try:
#         result = requests.get(url)
#         result.raise_for_status()
#         return result.text
#     except(requests.RequestException, ValueError):
#         print("Сетевая ошибка")
#         return False

# def get_python_news():
#     html = get_html("https://www.python.org/blogs/")
#     if html:     
#         soup = BeautifulSoup(html, 'html.parser')
#         all_news = soup.find('ul', class_='list-recent-posts').findAll('li')
#         result_news = []
#         for news in all_news:
#             title = news.find('a').text
#             url = news.find('a')['href']
#             published = news.find('time').text
#             result_news.append({
#                 "title": title,
#                 "url": url,
#                 "published": published
#             })
#         return result_news
#     return False