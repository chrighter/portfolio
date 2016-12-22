# from app import app

# @app.route('/')
# @app.route('/index')
# def index():
#	 return "Hello, World!"

# простое представление, которое просто возвращает строку для отображения в пользовательском браузере. 
# Два декоратора route создают привязку адресов / и /index к этой функции.

# from flask import render_template
# from app import app

# @app.route('/')
# @app.route('/index')
# def index():
#	 user = { 'nickname': 'Miguel' } # выдуманный пользователь
#	 return render_template("index.html",
#		 title = 'Home',
#		 user = user)

from flask import Flask, request, session, g, redirect, url_for, abort, render_template, flash, send_file, redirect, make_response
from app import app
from datetime import datetime
from contextlib import closing
import sqlite3
import json
from wand.image import Image
from wand.drawing import Drawing
from wand.color import Color
from io import BytesIO
import time
from functools import wraps, update_wrapper
#from sqlite3 import strftime
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

#conn = sqlite3.connect('./count.db')
d = dict()	 
@app.after_request
def after_request(response):
	badaddresses = ['/badbook', '/static/mystyles.css', '/static/RobotoCondensed.ttf', '/static/mail.ico', '/like', '/static/RobotoCondensed.ttf', '/static/vk.ico', '/static/inst.ico', '/static/icon2.ico', '/static/loadgif.gif','/static/bg1.jpg', '/favicon.ico', '/pictures/2pic.jpg', '/pictures/1pic.jpg', '/pictures/3pic.jpg', '/pictures/4pic.jpg', '/static/1picthumb.jpg', '/static/2picthumb.jpg', '/static/3picthumb.jpg', '/static/4picthumb.jpg']
	conn = sqlite3.connect('./lol.db')
	cursor = conn.cursor()
	try:
		cursor.execute("SELECT count(*) date, ip FROM visitors WHERE time - '{0}' < 60 and day = '{1}' GROUP BY ip".format( int(time.time()), str(datetime.now()).split()[0]))
		request_ip_in_munute = cursor.fetchone()

		if request_ip_in_munute[0] > 200:
			 d[request_ip_in_munute[1]] = int(time.time())

		if (request_ip_in_munute[1] in d and time.time() - d[request_ip_in_munute[1]] > 30 or request_ip_in_munute[1] not in d) and not(request.path in badaddresses) and re.match(r'^(?=.*\d)(?=.*[a-z])(?=.*[A-Z])(?!;\/\.*\s).*$', request.user_agent.string):

			cursor.execute("INSERT INTO visitors VALUES (?,?,?,?,?,?)", (request.remote_addr, datetime.now(), request.path, request.user_agent.string, str(datetime.now()).split()[0], str(time.time()).split('.')[0]))
			conn.commit()
			conn.close()
			try:
				del d[request_ip_in_munute[1]]
			except:
				pass
	except:			
		cursor.execute("INSERT INTO visitors VALUES (?,?,?,?,?,?)", (request.remote_addr, datetime.now(), request.path, request.user_agent.string, str(datetime.now()).split()[0], str(time.time()).split('.')[0]))
		conn.commit()
		conn.close()		
	return response

def nocache(view):
    @wraps(view)
    def no_cache(*args, **kwargs):
        response = make_response(view(*args, **kwargs))
        response.headers['Last-Modified'] = datetime.now()
        response.headers['Cache-Control'] = (
            'no-store, no-cache, must-revalidate, ' +
            'post-check=0, pre-check=0, max-age=0'
        )
        response.headers['Pragma'] = 'no-cache'
        response.headers['Expires'] = '-1'
        return response
 
    return update_wrapper(no_cache, view)


@app.route('/visitors')
@nocache
def visitors():
	conn = sqlite3.connect('./lol.db')
	cursor = conn.cursor()
	cursor.execute("SELECT count(*) FROM visitors")
	browsing = cursor.fetchone()[0]
	cursor.execute("SELECT count(*) FROM visitors WHERE day = '%s'" % (str(datetime.now()).split()[0]))
	browsing_today = cursor.fetchone()[0]
	cursor.execute("SELECT date, ip FROM visitors WHERE ip = '%s' GROUP BY ip" % (request.remote_addr))
	last_visit = cursor.fetchone()
	if not last_visit:
		last_visit = "Чуть-чуть не считается (0)"
	else:
		last_visit = last_visit[0][:-7] 	
	cursor.execute("SELECT count(*) FROM visitors WHERE ip = '{0}' AND {1} - time > 1800".format(request.remote_addr, time.time()))
	visits = cursor.fetchone()[0]
	cursor.execute("SELECT count(*) FROM visitors WHERE ip = '{0}' AND {1} - time > 1800 AND day = {2}".format(request.remote_addr, time.time(), str(datetime.now()).split()[0]))
	visits_today = cursor.fetchone()[0]
	img = Image(width=700, height=150)
	with Drawing() as draw:
		draw.fill_color=Color('black')
		draw.font_size=14
		draw.text(30,25, 'Всего просмотров: '+str(browsing))
		draw.text(30,50, 'Всего просмотров сегодня: '+str(browsing_today))
		draw.text(30,75, 'Всего посещений: '+str(visits))
		draw.text(30,100, 'Всего посещений сегодня: '+str(visits_today))
		draw.text(30,125, 'Дата последнего посещения: '+str(last_visit))
		draw(img)
	buffer = BytesIO()
	with img.convert('png') as converted:
		converted.save(buffer)
	buffer.seek(0)
	return send_file(buffer, mimetype='image/png')


@app.route('/statistic')
def statistic():
	conn = sqlite3.connect('./lol.db')
	cursor = conn.cursor()
	
	cursor.execute("SELECT * FROM visitors ORDER BY date DESC")
	data = cursor.fetchall()
	
	return render_template('statistic.html', data = data)

@app.route('/comment', methods=['POST', 'GET'])
def comment():
	if request.method == "POST":
		# print(request.form["nick"], request.form["content"])
		# print(request.form["nick"], request.form["mail"], request.form["content"])
		# валидация
		date = datetime.now()
		conn = sqlite3.connect('./comment.db')
		cursor = conn.cursor()
		if not request.form[botcheck]:
			cursor.execute("INSERT INTO comment VALUES (?,?,?)", (request.form["nick"], request.form["content"], str(datetime.now()).split()[0]))
			conn.commit()
			conn.close()
		return redirect("/comments")
	else:	
		return render_template('comment.html', title = 'comment')

@app.route('/comments', methods=['POST', 'GET'])
def comments():
	conn = sqlite3.connect('./comment.db')
	cursor = conn.cursor()
	cursor.execute("SELECT * FROM comment")
	data = cursor.fetchall()
	conn.commit()
	conn.close()	
	return render_template('comments.html', data=data)


@app.route('/checknick')
def ch():
	# response.headers["Access-Control-Allow-Origin"] = "*"
	name = request.GET.get("name", "").strip()
	result = re.match(r"{1,50}$", name)
	if result:
		data = ""
	else:
		data = "Некорректный формат данных, длина ника не может составлять более 50 знаков."
	return data 

@app.route('/badbook')
def badbook():
	return render_template('badbook.html')

conn = sqlite3.connect('./likes.db')
@app.route('/like', methods=['POST', 'GET'])
def like():
	if request.method == "POST":
		cursor = conn.cursor()
		cursor.execute("SELECT count FROM likes WHERE id = ?", (request.form["id"], ))
		result = cursor.fetchone()
		if result[0] < 0:
			count = count + (result[0]) * (-1)
		if not result:
			count = 1
			cursor.execute("INSERT INTO likes VALUES (?, ?)", (request.form["id"], 1))
		else:	
			count = result[0] + 1
			cursor.execute("DELETE FROM likes WHERE id = ?", (request.form["id"], ))
			cursor.execute("INSERT INTO likes VALUES (?, ?)", (request.form["id"], count))
		conn.commit()
		return str(count)
	else:
		cursor = conn.cursor()
		id = request.args.get("id", "").strip()
		print("ID",id)
		cursor.execute("SELECT count FROM likes WHERE id = ?", (id, ))
		result = cursor.fetchone()
		if not result:
			count = 0
		else:
			count = result[0]
		conn.commit()
		return str(count)
			
