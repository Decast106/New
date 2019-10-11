# from flask import Flask
# from weather import weather_by_city

# app = Flask(__name__)

# @app.route("/")
# def index():
#     weather = weather_by_city("Moscow,Russia")
#     # weather = False
#     if weather:
#         return f"Погода: {weather['temp_C']}, ощущается как {weather['FeelsLikeC']}"
#     else:
#         return 'Сервис погоды временно недоступен'


# if __name__ == '__main__':
#     app.run(debug=True)



from flask import Flask, render_template

from webapp.model import db, News
from webapp.weather import weather_by_city

def create_app():
    app = Flask(__name__)
    app.config.from_pyfile('config.py')
    db.init_app(app)

    @app.route("/")
    def index():
        title = 'Новости Python'
        weather = weather_by_city(app.config['WEATHER_DEFAULT_CITY'])
        news_list = News.query.order_by(News.published.desc()).all()
        return render_template('index.html', page_title=title, weather=weather, news_list=news_list)

    return app
