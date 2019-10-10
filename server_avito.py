from flask import Flask, render_template

from parser_avito import parse

app = Flask(__name__)

@app.route("/")
def index():
    title = '111'
    news_list = parse()
    return render_template('index_avito.html', page_title=title, news_list=news_list)


if __name__ == '__main__':
    app.run(debug=True)
