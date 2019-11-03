from webapp import create_app
from webapp.hh_2 import hh_parse
from flask import current_app


app = create_app()
with app.app_context():
    hh_parse(current_app.config['BASE_URL'], current_app.config['HEADERS'])