# from app import app

# @app.route('/')
# @app.route('/index')
# def index():
#     return "Hello, World!"

# простое представление, которое просто возвращает строку для отображения в пользовательском браузере. 
# Два декоратора route создают привязку адресов / и /index к этой функции.

# from flask import render_template
# from app import app

# @app.route('/')
# @app.route('/index')
# def index():
#     user = { 'nickname': 'Miguel' } # выдуманный пользователь
#     return render_template("index.html",
#         title = 'Home',
#         user = user)

from flask import render_template
from app import app

@app.route('/')
@app.route('/main')
def main():
    return render_template('main.html', title = 'main')

@app.route('/about')
def about():
    return render_template('about.html', title = 'about')

@app.route('/pictures/<image>')
@app.route('/pictures')
def pictures(image=None):
    return render_template('pictures.html', title = 'pictures')

@app.route('/help')
def help():
    return render_template('help.html', title = 'help')


