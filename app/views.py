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

from flask import Flask, request, session, g, redirect, url_for, abort, render_template, flash, send_file  
from app import app
from datetime import datetime
from contextlib import closing
import sqlite3
import json
from wand.image import Image
from wand.drawing import Drawing
from wand.color import Color
from io import BytesIO
#import nocache

DATABASE = '/counter.db'
DEBUG = True
SECRET_KEY = 'development key'
USERNAME = 'admin'
PASSWORD = 'default'
app.config.from_envvar('FLASKR_SETTINGS', silent=True)

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

@app.route('/robots.txt')
def robots():
    return send_file('robots.txt')    

            
@app.after_request
def after_request(response):
    conn = sqlite3.connect('./counter.db')
    conn.execute("CREATE TABLE IF NOT EXISTS visitors (ip TEXT, date INTEGER)");
    conn.execute("INSERT INTO visitors VALUES (?,?)", (request.remote_addr ,datetime.now()) )
    conn.commit()
    conn.close()
    return response


@app.route('/visitors')
#@nocache.nocache
def visitors():
    conn = sqlite3.connect('./counter.db')
    cursor = conn.cursor()
    cursor.execute("SELECT count(*) FROM visitors")
#    visits = cursor.fetchall()
    visits = cursor.fetchone()
    print('lalal', str(visitors['date']).split()[1].split()[0])
    cursor.execute("SELECT * FROM visitors where str(visitors[date]).split()[1].split()[0] = str(datetime.now()).split()[0] group by visitors.ip")
#    cursor.execute("SELECT * FROM visitors group by ip")
    data = cursor.fetchone()
    print(visits)
    print(data)
    print(type(data))
    print('kek', str(data).split()[1].split()[0])
    img = Image(width=300, height=350)
    print(visits[0], visits)
    with Drawing() as draw:
        draw.fill_color=Color('red')
        draw.text_alignment= 'center'
        draw.font_size=12
        draw.text(100,50, 'Количество просмотров: '+str(visits[0]))
        draw.text(100,50, 'Количество просмотров: ')
        
        draw(img)

#    img.save(filename='image01.jpg')
    buffer = BytesIO()
    with img.convert('png') as converted:
        converted.save(buffer)
    buffer.seek(0)
    return send_file(buffer, mimetype='image/png')


#    return send_file(byte_io, mimetype='image/png')
    # return render_template('visitors.html', visits=visits, title = 'visitors')

