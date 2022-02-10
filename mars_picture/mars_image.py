from flask import Flask, url_for

app = Flask(__name__)


@app.route('/')
def mission():
    return "Миссия Колонизация Марса"


@app.route('/index')
def motto():
    return "И на Марсе будут яблони цвести!"


@app.route('/promotion')
def promotion():
    frazes = ['Человечество вырастает из детства.',
              'Человечеству мала одна планета.',
              'Мы сделаем обитаемыми безжизненные пока планеты.',
              'И начнем с Марса!',
              'Присоединяйся!']
    return '<br>'.join(frazes)


@app.route('/image_mars')
def red_planet():
    return f'<title>Привет, Марс!</title>' \
           f'<h1>Жди нас, Марс!</h1>' \
           f'''<img src="{url_for("static", filename="img/mars.png")}"
           alt="здесь Марс" width="300" height="300">
           <br>Вот она какая, красная планета.'''


if __name__ == '__main__':
    app.run(port=8080, host='127.0.0.1')