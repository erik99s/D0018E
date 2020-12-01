from flask import Flask, redirect, url_for, render_template, flash, redirect, session, request
from forms import RegistrationForm, LoginForm
from flask_mysqldb import MySQLdb, MySQL
import sys, MySQLdb.cursors, re
from flask_sqlalchemy import SQLAlchemy
from flask_admin import Admin, AdminIndexView
from flask_admin.contrib.sqla import ModelView 

app = Flask(__name__)

app.config['SECRET_KEY'] = '1c15e0b9ef383e18d6ba8646275b4c88'  

#pip install flask
#pip install flask-wtf
#pip install flask-mysqldb
#pip install flask-mysql-connector

#config mySQL
app.config['MYSQL_HOST'] = "utbweb.its.ltu.se"
app.config['MYSQL_USER'] = "980705"
app.config['MYSQL_PASSWORD'] = "980705"
app.config['MYSQL_DB'] = 'db980705'
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://980705:980705@utbweb.its.ltu.se/db980705'

db = SQLAlchemy(app)
db.Model.metadata.reflect(bind=db.engine, schema='db980705')

class Customer(db.Model):
    __table__ = db.Model.metadata.tables['db980705.Customer']

admin = Admin(app)
admin.add_view(ModelView(Customer, db.session))

# init mySQL
mysql = MySQL(app)

@app.route("/")
@app.route("/home")
def home():
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute('SELECT * FROM Products')
    data = cursor.fetchall()
    return render_template("HomePage.html", data=data)


@app.route("/register", methods=['GET', 'POST'])
def register():
    msg = ''
    form = RegistrationForm()
    if form.validate_on_submit():
        if request.method == 'POST' and 'firstName' in request.form and 'lastName' in request.form and 'email' in request.form and 'confirm_email' in request.form and 'password' in request.form and 'confirm_password' in request.form:
            firstName = request.form['firstName']
            lastName = request.form['lastName']
            email = request.form['email']
            password = request.form['password']
            cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
            cursor.execute('SELECT * FROM Customer WHERE Email = %s', [email])
            account = cursor.fetchone()

            if account:
                msg = 'Account already exists!'

            else:
                cursor.execute('INSERT INTO Customer VALUES(NULL, %s, %s, %s, %s)', [firstName, lastName, email, password])
                mysql.connection.commit()
                msg = 'Successfully created account'
                flash(f'Account created for {form.email.data}!', 'success')
                return redirect(url_for('home'))

    elif request.method == 'POST':
        msg = 'Fill out form correctly'

    return render_template('RegisterPage.html', title='Register', form=form, msg=msg)        


@app.route("/login", methods=['GET', 'POST'])
def login():
    form = LoginForm()
    msg = ''

    #Get info from database
    if request.method == 'POST' and 'email' in request.form and 'password' in request.form:
        email = request.form['email']
        password = request.form['password']

        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM Customer WHERE Email = %s AND Password = %s', [email, password])
        data = cursor.fetchone()

        if data:
            session['loggedin'] = True
            session['id'] = data['CustomerID']
            return redirect(url_for('home'))
        else:
            msg = 'Does not recognize email/password'
            session['loggedin'] = False
            return render_template('LoginPage.html', title='login', form=form, msg=msg)
    
    return render_template('LoginPage.html', title='login', form=form, msg=msg)

@app.route("/logout", methods=['GET', 'POST'])
def logout():
    session.pop('loggedin', None)
    session.pop('id', None)
    return redirect(url_for('home'))

@app.route("/product.<string:id>")
def products(id):
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute('SELECT * FROM Products WHERE ProductID = %s', [id])
    data = cursor.fetchone()
    return render_template('ProductPage.html', data=data)

@app.route("/profile")
def profile():
    if 'loggedin' in session:
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM Customer WHERE CustomerID = %s', [session['id']])
        data = cursor.fetchone()
        return render_template('ProfilePage.html', data=data)
    
    return redirect(url_for('login'))

@app.route("/cart")
def cart():
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute('SELECT * FROM Cart WHERE CustomerID = %s', [session['id']])
    data = cursor.fetchall()
    products = []
    for row in data:
        cursor.execute('SELECT * FROM Products WHERE ProductID = %s', [row['ProductID']])
        product = cursor.fetchone()
        product.update({'Amount,' : row['Amount']})
        products.append(product)
    print(products)
    return render_template('CartPage.html', products=products)

@app.route("/addToCart.<string:id>")
def addToCart(id):
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute('INSERT INTO Cart VALUES(%s, %s, %s)', [session['id'], id, 1])
    mysql.connection.commit()
    return redirect(url_for('home'))
    
if __name__ == "__main__":
    app.run(debug=True)