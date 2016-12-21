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
import time


conn = sqlite3.connect('./likes.db')
conn.execute("CREATE TABLE IF NOT EXISTS likes (id TEXT, count INT)")
conn.commit()
conn.close()
print('БД likes инициализирована')
