from flask import Flask, redirect, url_for, render_template, flash, redirect, session, request
from forms import RegistrationForm, LoginForm
from flask_mysqldb import MySQLdb, MySQL
from flask_mysql_connector import mysql
import sys, MySQLdb.cursors, re

#run
app = Flask(__name__)

app.config['SECRET_KEY'] = '1c15e0b9ef383e18d6ba8646275b4c88'  

# config mySQL
app.config['MYSQL_HOST'] = "localhost"
app.config['MYSQL_USER'] = "root"
app.config['MYSQL_PASSWORD'] = ""
app.config['MYSQL_DB'] = 'mydb'

# init mySQL
mysql = MySQL(app)

@app.route("/")
@app.route("/home")
def home():
    return render_template("HomePage.html")


@app.route("/register", methods=['GET', 'POST'])
def register():
    msg = ''
    form = RegistrationForm()
    if form.validate_on_submit():
        if request.method == 'POST' and 'firstName' in request.form and 'lastName' in request.form and 'email' in request.form and 'repeatEmail' in request.form and 'password' in request.form and 'repeatPassword' in request.form:
            firstName = request.form['firstName']
            lastName = request.form['lastName']
            email = request.form['email']
            password = request.form['password']
            cursor = mysql.connection.cursor(MySQLdb.cursor.DictCursor)
            cursor.execute('SELECT * FROM accounts WHERE email = %s',(email,))
            account = cursor.fetchone()

            if account:
                msg = 'Account already exists!'
            else:
                cursor.execute('INSERT INTO accounts VALUES(NULL, %s, %s, %s, %s)', (firstName, lastName, email, password))
                mysql.connection.commit()
                msg = 'Successfully created account'
                flash(f'Account created for {form.email.data}!', 'success')
                return redirect(url_for('home'))

        elif request.method == 'POST':
            msg = 'fill out form correctly'

    return render_template('RegisterPage.html', title='Register', form=form, msg=msg)        


@app.route("/login", methods=['GET', 'POST'])
def login():
    form = LoginForm()
    msg = ''

    #Get info from database
    if request.method == 'POST' and 'email' in request.form and 'password' in request.form:
        email = request.form['email']
        password = request.form['password']

        cursor = mysql.connection.cursor(MySQLdb.cursor.DictCursor)
        cursor.execute('SELECT * FROM accounts WHERE email = %s AND password = %s', (email, password,))
        account = cursor.fetchone()

        if account:
            session['loggedin'] = True
            session['id'] = account['id']
            session['email'] = account['email']
            return render_template('HomePage.html', title='home', form=form, msg=msg)
        else:
            msg = 'Does not recognize email/password'
            session['logged_in'] = False
            return render_template('LoginPage.html', title='login', form=form, msg=msg)

@app.route("/loggedIn")
def loggedIn():
    if 'loggedin' in session:
        return render_template('LoggedInPage.html', title='loggedIn')
    return redirect(url_for('homePage.html'))

    
@app.route("/product")
def products():
    return render_template('ProductPage.html', title='product')

@app.route("/profile")
def profile():
    if 'loggedin' in session:
        cursor = mysql.connection.cursor(MySQLdb.cursor.DictCursor)
        cursor.execute('SELECT * FROM accounts WHERE id = %s', (session['id']))
        account = cursor.fetchone()
        return render_template('ProfilePage.html', account=account)
    
    return redirect(url_for('loggedInPage'))

if __name__ == "__main__":
    app.run(debug=True)

