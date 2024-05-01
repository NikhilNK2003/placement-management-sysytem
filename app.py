#app.py

from flask import Flask
from config import SECRET_KEY, MYSQL_HOST, MYSQL_USER, MYSQL_PASSWORD, MYSQL_DB
from flask_mysqldb import MySQL

app = Flask(__name__)
app.secret_key = 'your secret key'
app.config['MYSQL_HOST'] = MYSQL_HOST
app.config['MYSQL_USER'] = MYSQL_USER
app.config['MYSQL_PASSWORD'] = MYSQL_PASSWORD
app.config['MYSQL_DB'] = MYSQL_DB
mysql = MySQL(app)
from routes import *

if __name__ == "__main__":
	app.run(debug=True)