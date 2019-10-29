from flask import Flask, render_template

from hh_2 import hh_parse

app = Flask(__name__)

@app.route("/")
def index():
    title = 'Вакансии "Junior Python Developer" за три дня - парсинг с HH.ru'
    headers = {'accept': '*/*',
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:70.0) Gecko/20100101 Firefox/70.0'}
    base_url = 'https://hh.ru/search/vacancy?area=1&search_period=3&text=Junior+Python+Developer&page=0'
    vacance_list = hh_parse(base_url, headers)
    return render_template('index.html', page_title=title, vacance_list=vacance_list)


if __name__ == '__main__':
    app.run(debug=True)
