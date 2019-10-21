from bs4 import BeautifulSoup
import requests


def get_html(url):
	try:
		result = requests.get(url=url)
		result.raise_for_status()
		return result.text
	except(requests.RequestException):
		return 'Ссылка временно не доступна, Ответ не возможен'

def parse(html):
	soup = BeautifulSoup(html, 'html.parser')
	items = soup.find('div', class_='item-with-contact')
	return items


if __name__ == "__main__":
	url = "https://www.avito.ru/moskva/tovary_dlya_kompyutera/komplektuyuschie/videokarty?p=70"
	html = get_html(url)
	news = parse(html)
	print(news)	















# import requests
# from bs4 import BeautifulSoup

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












	# avito_url = "https://www.avito.ru/moskva/tovary_dlya_kompyutera/komplektuyuschie/videokarty?p=90"
	# print(connect_to_avito(avito_url))

	# avito_url = "https://www.avito.ru/moskva/tovary_dlya_kompyutera/komplektuyuschie/videokarty?p=100"
	# print(connect_to_avito(avito_url))





# try:
#     result = requests.get(weather_url, params=params)
#     result.raise_for_status()
#     return result.json()
#     ...
# except(requests.RequestException):
#     return False






# import requests

# def weather_by_city(city_name):
#     weather_url = "http://api.worldweatheronline.com/premium/v1/weather.ashx"
#     params = {
#         "key": "3f58b2c6faa7436087d163348192009",
#         "q": city_name,
#         "format": "json",
#         "num_of_days": 1,
#         "lang": "ru"
#     }
#     result = requests.get(weather_url, params=params)
#     weather = result.json()
#     if 'data' in weather:
#         if 'current_condition' in weather['data']:
#             try:
#                 return weather['data']['current_condition'][0]
#             except(IndexError, TypeError):
#                 return False
#     return False

# if __name__ == "__main__":
#     print(weather_by_city("Moscow,Russia"))




# import requests

# def connect_to_avito(url, a2 = 0):
# 	print(url, a2)
# 	try:
# 		result = requests.get(url=url)
# 		return result, 'ghbdtn'
# 	except(requests.RequestException):
# 		return 'Ссылка временно не доступна, Ответ не возможен'
