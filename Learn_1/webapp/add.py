
from datetime import datetime

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

def int_value_from_ru_month(date_str):
    return RU_MONTH_VALUES.get(date_str)

data = "31 октября"
print(data.split())
day, month = data.split()
print(datetime(year=datetime.now().year, month=int_value_from_ru_month(month), day=int(day)))


from flask import Flask, render_template, make_response
from webapp.model import db, Vacancy

def create_app():
    app = Flask(__name__)
    app.config.from_pyfile('config.py')
    db.init_app(app)

    @app.route("/")
    def index():
        title = app.config['TITLE']

        vacancies_list = Vacancy.query.order_by(Vacancy.data.desc()).all()
        return render_template('index.html', page_title=title, vacancies_list=vacancies_list)

    @app.route("/update")
    def update():
        headers = app.config['HEADERS']
        base_url =  app.config['BASE_URL']
        hh_parse(base_url, headers)
        return app.make_response('Hello, World')

    return app

from flask import Flask
app = Flask(name)
app.make_response('Hello, World')
<Response 12 bytes [200 OK]>