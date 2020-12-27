from flask import Flask, redirect, url_for, render_template, flash, redirect, session, request
from forms import RegistrationForm, LoginForm, AddToCartForm, ratingForm
from flask_mysqldb import MySQLdb, MySQL
import sys, MySQLdb.cursors, re
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.sql import func
from flask_admin import Admin, AdminIndexView
from flask_admin.menu import MenuLink
from flask_admin.contrib.sqla import ModelView 

app = Flask(__name__)

app.config['SECRET_KEY'] = '1c15e0b9ef383e18d6ba8646275b4c88'  

#config mySQL
app.config['MYSQL_HOST'] = "utbweb.its.ltu.se"
app.config['MYSQL_USER'] = "980705"
app.config['MYSQL_PASSWORD'] = "980705"
app.config['MYSQL_DB'] = 'db980705'
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://980705:980705@utbweb.its.ltu.se/db980705'

db = SQLAlchemy(app)
db.Model.metadata.reflect(bind=db.engine, schema='db980705')

class AdminIndexView(AdminIndexView):
     def is_accessible(self):
        try:
            cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
            cursor.execute('SELECT * FROM Admin WHERE CustomerID = %s', [session['id']])
            account = cursor.fetchone()
            if account:
                return True
        except:  # Gets in except if id is not in session, meaning that the user is not logged in
            return False
        return False  # This returns false only if a user is logged in, but not admin

class AdminUser(db.Model):
    __table__ = db.Model.metadata.tables['db980705.Admin']

class AdminUserView(ModelView):
    column_list = ('CustomerID', 'DateOfAdmin')
    def is_accessible(self):
        try:
            cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
            cursor.execute('SELECT * FROM Admin WHERE CustomerID = %s', [session['id']])
            account = cursor.fetchone()
            if account:
                return True
        except:  # Gets in except if id is not in session, meaning that the user is not logged in
            return False
        return False  # This returns false only if a user is logged in, but not admin

class Customer(db.Model):
    __table__ = db.Model.metadata.tables['db980705.Customer']

class CustomerView(ModelView):
     def is_accessible(self):
        try:
            cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
            cursor.execute('SELECT * FROM Admin WHERE CustomerID = %s', [session['id']])
            account = cursor.fetchone()
            if account:
                return True
        except:  # Gets in except if id is not in session, meaning that the user is not logged in
            return False
        return False  # This returns false only if a user is logged in, but not admin

class Products(db.Model):
    __table__ = db.Model.metadata.tables['db980705.Products']

class ProductsView(ModelView):
    def is_accessible(self):
        try:
            cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
            cursor.execute('SELECT * FROM Admin WHERE CustomerID = %s', [session['id']])
            account = cursor.fetchone()
            if account:
                return True
        except:  # Gets in except if id is not in session, meaning that the user is not logged in
            return False
        return False  # This returns false only if a user is logged in, but not admin

#class Cart(db.Model):
#    __table__ = db.Model.metadata.tables['db980705.Cart']

#class Reviews(db.Model):
#    __table__ = db.Model.metadata.tables['db980705.Reviews']

admin = Admin(app, name="Desire", index_view = AdminIndexView())
admin.add_view(AdminUserView(AdminUser, db.session, 'Admin'))
admin.add_view(CustomerView(Customer, db.session))
admin.add_view(ProductsView(Products, db.session))
#admin.add_view(ModelView(Cart, db.session))
#admin.add_view(ModelView(Reviews, db.session))
admin.add_link(MenuLink(name='Profile', category='', url="/profile"))
admin.add_link(MenuLink(name='Logout', category='', url="/logout"))

# init mySQL
mysql = MySQL(app)

@app.route("/")
@app.route("/home")
def home():
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute('SELECT * FROM Products')
    data = cursor.fetchall()
    return render_template("HomePage.html", data=data)

@app.route("/admin")  
def admin():
    return None


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
    product = cursor.fetchone()
    cursor.execute('SELECT * FROM Reviews WHERE ProductID = %s', [id])
    reviews = cursor.fetchall()

    #TO DO: ändra till average av Reviews.Rating (funkar inte i stunden)
    result = db.session.query(func.avg(Customer.CustomerID))
    print(result)

    for row in reviews:
        cursor.execute('SELECT * FROM Customer WHERE CustomerID = %s', [row['CustomerID']])
        customer = cursor.fetchone()
        row.update({'FirstName' : customer['FirstName']})
        row.update({'LastName' : customer['LastName']})
    return render_template('ProductPage.html', product=product, reviews=reviews, result=result)

@app.route("/profile")
def profile():
    if 'loggedin' in session:
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM Customer WHERE CustomerID = %s', [session['id']])
        data = cursor.fetchone()
        cursor.execute('SELECT * FROM Reviews WHERE CustomerID = %s', [session['id']])
        reviews = cursor.fetchall()
        return render_template('ProfilePage.html', data=data, reviews=reviews)
    
    return redirect(url_for('login'))

@app.route("/cart")
def cart():
    try:
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT ProductID, Amount FROM Cart WHERE CustomerID = %s', [session['id']])
        data = cursor.fetchall()
        products = []
        for row in data:
            cursor.execute('SELECT * FROM Products WHERE ProductID = %s', [row['ProductID']])
            product = cursor.fetchone()
            product.update({'Amount' : row['Amount']})
            products.append(product)
        return render_template('CartPage.html', products=products)
    except:
        return redirect(url_for('login'))

@app.route("/addToCart.<string:id>", methods=['GET', 'POST'])
def addToCart(id):
    try:
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)

        form = AddToCartForm()
        try:
            amount = int(request.form['productAmount'])
        except:
            amount = 1 

        try:
            cursor.execute('INSERT INTO Cart VALUES(%s, %s, %s)', [session['id'], id, amount])
            cursor.execute('UPDATE Cart SET Amount = Amount + %s WHERE CustomerID = %s and ProductID = %s', [amount, session['id'], id])
        except:
            cursor.execute('INSERT INTO Cart VALUES(%s, %s, %s)', [session['id'], id, amount])
        mysql.connection.commit()
     
    except:
        return redirect(url_for('home'))
    return redirect(request.referrer)

@app.route("/removeFromCart.<string:id>")
def removeFromCart(id):
    try:
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('DELETE FROM Cart WHERE CustomerID = %s and ProductID = %s', [session['id'], id])
        mysql.connection.commit()
        return redirect(url_for('cart'))
    except:
        return redirect(url_for('home'))

@app.route("/removeOneFromCart.<string:id>")
def removeOneFromCart(id):
    try:
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('UPDATE Cart SET Amount = Amount - 1 WHERE CustomerID = %s and ProductID = %s', [session['id'], id])
        cursor.execute('DELETE FROM Cart WHERE Amount = 0')
        mysql.connection.commit()
        return redirect(request.referrer)
    except:
        return redirect(url_for('home'))

@app.route("/clearCart")
def clearCart():
    try:
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('DELETE FROM Cart WHERE CustomerID = %s', [session['id']])
        mysql.connection.commit()
    except:
        return redirect(url_for('home'))
    return redirect(request.referrer)

@app.route("/rateProduct.<string:id>", methods=['GET', 'POST'])
def rateProduct(id):
    try:
        form = ratingForm()
        comment = request.form['comment']
        title = request.form['title']
        rating = request.form['star']
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM Reviews WHERE CustomerID = %s AND ProductID = %s', [session['id'], id])
        data = cursor.fetchone()

        if data:
            cursor.execute('UPDATE Reviews SET Comment = %s, Title = %s, Rating = %s WHERE CustomerID = %s and ProductID = %s', [comment, title, rating ,session['id'], id])
        else:
            cursor.execute('INSERT INTO Reviews VALUES(%s, %s, %s, %s, %s, NULL)', [session['id'], id, comment, title, rating])
        mysql.connection.commit()

    except:
        return redirect(url_for('home'))
    return redirect(request.referrer)

@app.route("/deleteReview.<string:id>")
def deleteReview(id):
    try:
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('DELETE FROM Reviews WHERE CustomerID = %s and ProductID = %s', [session['id'], id])
        mysql.connection.commit()
    except:
        return redirect(url_for('home'))
    return redirect(request.referrer)

@app.route("/checkOut")
def checkOut():
    if 'loggedin' in session:
        return render_template('CheckOutPage.html')
    return redirect(url_for('login'))

if __name__ == "__main__":
    app.run(debug=True)
