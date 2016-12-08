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

from flask import Flask, request, session, g, redirect, url_for, abort, render_template, flash, send_file, redirect
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
	conn = sqlite3.connect('./lol.db')
	cursor = conn.cursor()
	try:
		cursor.execute("SELECT count(*) date, ip FROM visitors WHERE time - '{0}' < 60 and day = '{1}' GROUP BY ip".format( int(time.time()), str(datetime.now()).split()[0]))
		request_ip_in_munute = cursor.fetchone()
		print('minute', request_ip_in_munute)
		print('kek', str(time.time()).split('.')[0])
		if request_ip_in_munute[0] > 100:
			 d[request_ip_in_munute[1]] = int(time.time())
		print('d', d)	 
		print('time', time.time())
		if request_ip_in_munute[1] in d and time.time() - d[request_ip_in_munute[1]] > 30 or request_ip_in_munute[1] not in d:
			conn.execute("INSERT INTO visitors VALUES (?,?,?,?,?,?)", (request.remote_addr, datetime.now(), request.path, request.user_agent.string, str(datetime.now()).split()[0], str(time.time()).split('.')[0]))
			conn.commit()
			conn.close()
			try:
				del d[request_ip_in_munute[1]]
			except:
				pass
	except:			
		conn.execute("INSERT INTO visitors VALUES (?,?,?,?,?,?)", (request.remote_addr, datetime.now(), request.path, request.user_agent.string, str(datetime.now()).split()[0], str(time.time()).split('.')[0]))
		conn.commit()
		conn.close()		
	return response



#conn = sqlite3.connect('./count.db')
@app.route('/visitors')
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
	
	cursor.execute("SELECT * FROM visitors")
	data = cursor.fetchall()
	
	return render_template('statistic.html', data = data)

@app.route('/comment', methods=['POST', 'GET'])
def comment():
	if request.method == "POST":
		print(request.form["nick"], request.form["content"])
		# print(request.form["nick"], request.form["mail"], request.form["content"])
		# валидация 
		conn = sqlite3.connect('./comment.db')
		cursor = conn.cursor()
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


# conn = sqlite3.connect('comments.db')
# users = dict()
# data = ''
# @app.route('/pushdata', methods=['POST', 'GET'])
# def push():
# 	# print("aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa")
# 	# print('request.POST.content', request.POST["content"]) 
# 	# if request.POST["nick"] and request.POST["mail"] and request.POST["content"]:
# 	# 	cursor = conn.cursor()
# 	# 	if (not (request.POST.nick in users) and not(request.POST.nick in stopwords)) and not(request.POST.mail in users.values()) and (re.match(r"[A-Za-z\d]{1,50}$", request.POST.nick)) and (re.match(r"^[-\w.]+@([A-z0-9][-A-z0-9]+\.)+[A-z]{2,4}$", request.POST.mail)):
# 	# 		users[request.POST.nick] = request.POST.mail
# 	# 		cursor.execute("INSERT INTO users (nick, mail) VALUES (?, ?)", (request.POST.nick, request.POST.mail))
# 	# 		conn.commit()
# 	# 		data = "Поздравляем с успешной регистрацией"
# 	# 	else:
# 	# 		if request.POST.nick == "Serezha" or request.POST.nick == "serezha":
# 	# 			data = "Сережка иди нафиг"
# 	# 		elif request.POST.nick == "Misha" or request.POST.nick == "misha":
# 	# 			data = "Миша ухади"	
# 	# 		elif request.POST.nick in users:
# 	# 			data = "Пользователь с таким ником уже существует"
# 	# 		elif request.POST.mail in users.values():
# 	# 			data = "Пользователь с таким же адресом электронной почты уже существует"	
# 	# 		elif request.POST.nick == "admin" or request.POST.nick == "administrator":
# 	# 			data = "Недопустимый ник"
# 	# 		elif not re.match(r"[A-Za-z\d]{1,50}$", request.POST.nick):
# 	# 			data = "Содержимое поля 'Ник' содержит недопустимые символы"
# 	# 		elif not re.match(r"^[-\w.]+@([A-z0-9][-A-z0-9]+\.)+[A-z]{2,4}$", request.POST.mail):
# 	# 			data = "Содержимое поля 'E-mail' содержит недопустимые символы"		
# 	# 		else:
# 	# 			data = 'kek'		
# 	# else:
# 	# 	data = "Ошибка. Не переживайте, это случается и с лучшими из нас"
# 	# return data
# 	name=request.form['nick']
# 	content=request.form['content']
# 	print("content", content)
# 	return "content"
