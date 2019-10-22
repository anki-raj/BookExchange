from flask import Flask, request, render_template,url_for,redirect,session,flash
# from db_config import mysql
import bcrypt
from flask_mysqldb import MySQL,MySQLdb
app = Flask(__name__)
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'ankit'
app.config['MYSQL_PASSWORD'] = 'ankitraj'
app.config['MYSQL_DB'] = 'bookExchange'

mysql = MySQL(app)
@app.route('/')
def home():
    return render_template('home.html')


@app.route('/register',methods=['GET','POST'])
def register():
    if request.method == 'GET':
        return render_template('register.html')
    else:
        name = request.form['name']
        email = request.form['email']
        password = request.form['password'].encode('utf-8')
        hash_pass = bcrypt.hashpw(password, bcrypt.gensalt())
        sem = request.form['sem']
        usn = request.form['usn']

        cur = mysql.connection.cursor()
        cur.execute("INSERT INTO user (user_name, user_pass,user_mail,semester,usn) VALUES (%s,%s,%s,%s,%s)",(name, hash_pass,email,int(sem),usn,))
        mysql.connection.commit()
        return redirect(url_for('login'))

@app.route('/login',methods=['GET','POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password'].encode('utf-8')

        curl = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        curl.execute("SELECT * FROM user WHERE user_mail=%s",(email,))
        user = curl.fetchone()
        curl.close()

        if user != None and len(user) > 0:
            if bcrypt.hashpw(password, user["user_pass"].encode('utf-8')) == user["user_pass"].encode('utf-8'):
                session['name'] = user['user_name']
                session['email'] = user['user_mail']
                return render_template("home.html")
            else:
                return "password and email does not match"
        else:
            return "User not found."
    else:
        return render_template("login.html")


@app.route('/logout', methods=["GET", "POST"])
def logout():
    session.clear()
    return render_template("home.html")

@app.route('/borrow', methods= ['GET','POST'])
def borrow():
    curl = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    curl.execute("SELECT * from book")
    book = curl
    curl.close()
    return render_template('borrow.html', book = book)

@app.route('/lend',methods=['GET','POST'])
def lend():
    if request.method == 'GET':
        return render_template('lend.html')
    else:
        # flash(f"You have successfully added the book!")
        book_name = request.form['name']
        book_sub = request.form['subject']
        contact = request.form['contact']
        semester = request.form['semester']
        book_id = request.form['bookid']
        cur = mysql.connection.cursor()
        cur.execute("INSERT into book (book_id,book_name,contact_detail,book_sub,semester) VALUES (%s,%s,%s,%s,%s)",(book_id,book_name,contact,book_sub,semester))
        mysql.connection.commit()
        return render_template('home.html')


if __name__ == "__main__":
    app.config['SECRET_KEY'] = "mysecretkey"
    app.run(debug=True)
