from app import app
from flask_mysqldb import MySQL

app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'ankit'
app.config['MYSQL_PASSWORD'] = 'ankitraj'
app.config['MYSQL_DB'] = 'bookExchange'

mysql = MySQL(app)
