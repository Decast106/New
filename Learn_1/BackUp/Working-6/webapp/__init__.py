from flask import Flask, render_template
from webapp.model import db, Vacancy

def create_app():
    app = Flask(__name__)
    app.config.from_pyfile('config.py')
    db.init_app(app)

    @app.route("/")
    def index():
        title = app.config['TITLE']
        # headers = app.config['HEADERS']
        # base_url =  app.config['BASE_URL']
        # vacance_list = hh_parse(base_url, headers)
        vacancies_list = Vacancy.query.all()
        return render_template('index.html', page_title=title, vacancies_list=vacancies_list)
    return app



