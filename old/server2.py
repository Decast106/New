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
from weather import weather_by_city

app = Flask(__name__)

@app.route("/")
def index():
    title = 'Прогноз погоды'
    weather = weather_by_city("Moscow,Russia")
    if weather:
        weather_text = f'Погода: {weather['temp_C']}, ощущается как {weather['FeelLikeC']}'
    else:
        weather_text = 'Сервис погоды временно недоступен'
    return render_template('index.html', page_title=title, weather_text=weather_text)

    # weather = False
    # return render_template('index.html', page_title=title, weather=weather)


if __name__ == '__main__':
    app.run(debug=True)
