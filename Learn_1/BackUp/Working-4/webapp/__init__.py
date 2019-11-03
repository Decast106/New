from flask import Flask, render_template
from webapp.model import db
from webapp.hh_2 import hh_parse

def create_app():
    app = Flask(__name__)
    app.config.from_pyfile('config.py')
    db.init_app(app)

    @app.route("/")
    def index():
        title = app.config['TITLE']
        headers = app.config['HEADERS']
        base_url =  app.config['BASE_URL']
        vacance_list = hh_parse(base_url, headers)
        return render_template('index.html', page_title=title, vacance_list=vacance_list)

    return app



