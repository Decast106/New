from flask import Flask, render_template

from parser_avito import parse, get_html

app = Flask(__name__)

@app.route("/")
def index():
    title = '111'
    url = "https://www.avito.ru/moskva/tovary_dlya_kompyutera/komplektuyuschie/videokarty?p=70"
    html = get_html(url)
    news_list = parse(html)
    return render_template('index_avito.html', page_title=title, news_list=news_list)


if __name__ == '__main__':
    app.run(debug=True)
