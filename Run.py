from flask import Flask, redirect, url_for, render_template, flash, redirect, session, request
from forms import RegistrationForm, LoginForm, AddToCartForm, ratingForm, CheckOutForm, UpdateForm
from flask_mysqldb import MySQLdb, MySQL
import sys, MySQLdb.cursors, re
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.sql import func
from flask_admin import Admin, AdminIndexView, form
from flask_admin.menu import MenuLink
from flask_admin.contrib.sqla import ModelView
import os 

app = Flask(__name__)

app.config['SECRET_KEY'] = '1c15e0b9ef383e18d6ba8646275b4c88'  

#config mySQL
app.config['MYSQL_HOST'] = "utbweb.its.ltu.se"
app.config['MYSQL_USER'] = "980705"
app.config['MYSQL_PASSWORD'] = "980705"
app.config['MYSQL_DB'] = 'db980705'
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://980705:980705@utbweb.its.ltu.se/db980705'
app.config['FLASK_ADMIN_SWATCH'] = 'darkly'

basedir = os.path.abspath(os.path.dirname(__file__))
file_path = os.path.join(basedir, 'static/images')

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
    Customer_ID = db.relationship("Customer")

class AdminUserView(ModelView):
    column_list = ('Customer_ID', 'DateOfAdmin')
    form_columns = ['Customer_ID']

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
    
    def __repr__(self):
        return "%s, %s" % (self.FirstName, self.CustomerID)

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
    Category_ID = db.relationship("Category")

    def __repr__(self):
        return "%s, %s" % (self.ProductName, self.ProductID)

class ProductsView(ModelView):
    column_list = ('ProductID', 'ProductName', 'Category_ID', 'Price', 'InStock', 'ProductPicture', 'Description')
    form_columns = ('ProductName', 'Category_ID', 'Price', 'InStock', 'ProductPicture', 'Description')

    form_extra_fields = {
        'ProductPicture': form.ImageUploadField(
            'Picture', base_path=file_path)
    }

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

class Reviews(db.Model):
    __table__ = db.Model.metadata.tables['db980705.Reviews']
    Customer_ID = db.relationship("Customer")
    Product_ID = db.relationship("Products")

class ReviewsView(ModelView):
    column_list = ('Customer_ID', 'Product_ID', 'Comment', 'Title', 'Rating', 'Date')
    form_columns = ('Customer_ID', 'Product_ID', 'Comment', 'Title', 'Rating')

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

class Cart(db.Model):
    __table__ = db.Model.metadata.tables['db980705.Cart']
    Customer_ID = db.relationship("Customer")
    Product_ID = db.relationship("Products")

class CartView(ModelView):
    column_list = ('Customer_ID', 'Product_ID', 'Amount')

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

class Orders(db.Model):
    __table__ = db.Model.metadata.tables['db980705.Orders']
    Customer_ID = db.relationship("Customer")

class OrdersView(ModelView):
    column_list = ('OrderID', 'Customer_ID', 'TotalPrice', 'Country', 'City', 'ZIPcode', 'Address')

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

class OrderDetails(db.Model):
    __table__ = db.Model.metadata.tables['db980705.OrderDetails']
    Product_ID = db.relationship("Products")

class OrderDetailsView(ModelView):
    column_list = ('OrderID', 'Product_ID', 'Amount')
    
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

class PurchaseHistory(db.Model):
    __table__ = db.Model.metadata.tables['db980705.PurchaseHistory']
    Customer_ID = db.relationship("Customer")

class PurchaseHistoryView(ModelView):
    column_list = ('Customer_ID', 'ProductName', 'Price', 'ProductPicture', 'Amount')

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

class Category(db.Model):
    __table__ = db.Model.metadata.tables['db980705.Category']

    def __repr__(self):
        return "%s, %s" % (self.CategoryName, self.CategoryID)

class CategoryView(ModelView):

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

admin = Admin(app, name="Desire", index_view = AdminIndexView(), template_mode='bootstrap3')
admin.add_view(AdminUserView(AdminUser, db.session, 'Admin'))
admin.add_view(CustomerView(Customer, db.session))
admin.add_view(ProductsView(Products, db.session))
admin.add_view(ReviewsView(Reviews, db.session))
admin.add_view(CartView(Cart, db.session))
admin.add_view(OrdersView(Orders, db.session))
admin.add_view(OrderDetailsView(OrderDetails, db.session))
admin.add_view(PurchaseHistoryView(PurchaseHistory, db.session))
admin.add_view(CategoryView(Category, db.session))

admin.add_link(MenuLink(name='Home', category='', url="/home"))
admin.add_link(MenuLink(name='Logout', category='', url="/logout"))

# init mySQL
mysql = MySQL(app)

@app.route("/")
@app.route("/home")
@app.route("/home.<string:id>")
def home(id=None):
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute('SELECT * FROM Category')
    categories = cursor.fetchall()

    if id:
        cursor.execute('SELECT * FROM Products WHERE CategoryID = %s', [id])
    else:
        cursor.execute('SELECT * FROM Products')
    data = cursor.fetchall()

    return render_template("HomePage.html", data=data, categories=categories)
    
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
        msg = 'Failed to create account, Please fill out form correctly'
        return render_template('RegisterPage.html', title='Register', form=form, msg=msg)        

    return render_template('RegisterPage.html', title='register', form=form, msg=msg)

@app.route("/updateProfile", methods=['GET', 'POST'])
def updateProfile():
    form = UpdateForm()
    msg = ''
    
    if 'loggedin' in session:
        if form.validate_on_submit():
            if request.method == 'POST' and 'firstName' in request.form and 'lastName' in request.form and 'email' in request.form and 'confirm_email' in request.form and 'password' in request.form and 'confirm_password' in request.form:

                firstName = request.form['firstName']
                lastName = request.form['lastName']
                email = request.form['email']
                password = request.form['password']

                cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
                cursor.execute('UPDATE Customer SET FirstName = %s, LastName = %s, Email = %s, Password = %s WHERE CustomerID = %s', [firstName, lastName, email, password, session['id']])
                
                mysql.connection.commit()
                msg = 'Successfully created account'
                flash(f'Account successfully updated!', 'success')

                return redirect(url_for('profile'))

        elif request.method == 'POST':
            msg = 'Failed to update account, Please fill out form correctly'
        
        return render_template('RegisterPage.html', title='Register', form=form, msg=msg) 
    return redirect(url_for('login'))

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
            session['isAdmin'] = False

            #Check if customer is admin
            cursor.execute('SELECT * FROM Admin WHERE CustomerID = %s', [session['id']])
            if cursor.fetchone():
                session['isAdmin'] = True

            return redirect(url_for('home'))
        else:
            msg = 'Does not recognize email/password'
            return render_template('LoginPage.html', title='login', form=form, msg=msg)
    return render_template('LoginPage.html', title='login', form=form, msg=msg)

@app.route("/logout")
def logout():
    session.pop('loggedin', None)
    session.pop('id', None)
    session.pop('isAdmin', None)
    flash(f'Succesfully logged out!', 'success')
    return redirect(url_for('home'))

@app.route("/product.<string:id>")
def products(id):
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute('SELECT * FROM Products WHERE ProductID = %s', [id])
    product = cursor.fetchone()
    cursor.execute('SELECT * FROM Reviews WHERE ProductID = %s', [id])
    reviews = cursor.fetchall()

    #Calculate the average rating
    result = db.session.query(func.avg(Reviews.Rating)).filter(Reviews.ProductID == [id]).scalar()

    #If result equals NULL set it to 0
    if not result:
        result = 0

    #Get customers full name
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

        #Get customer information
        cursor.execute('SELECT * FROM Customer WHERE CustomerID = %s', [session['id']])
        data = cursor.fetchone()

        #Get customer reviews
        cursor.execute('SELECT * FROM Reviews WHERE CustomerID = %s', [session['id']])
        reviews = cursor.fetchall()

        #Get purchase history
        cursor.execute('SELECT * FROM PurchaseHistory WHERE CustomerID = %s', [session['id']])
        purchase = cursor.fetchall()

        return render_template('ProfilePage.html', data=data, reviews=reviews, purchase=purchase)
    else:
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
            amount = int (request.form['productAmount'])
        except:
            amount = 1 

        cursor.execute('SELECT * FROM Cart WHERE CustomerID = %s and ProductID = %s', [session['id'], id])
        if cursor.fetchone():
            cursor.execute('UPDATE Cart SET Amount = Amount + %s WHERE CustomerID = %s and ProductID = %s', [amount, session['id'], id])
        else:
            cursor.execute('INSERT INTO Cart VALUES(NULL, %s, %s, %s)', [session['id'], id, amount])

        mysql.connection.commit()
        return redirect(request.referrer)
    except:
        return redirect(url_for('home'))

@app.route("/removeFromCart.<string:id>")
def removeFromCart(id):
    try:
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('DELETE FROM Cart WHERE CustomerID = %s and ProductID = %s', [session['id'], id])

        mysql.connection.commit()
        return redirect(request.referrer)
    except:
        return redirect(url_for('home'))

@app.route("/removeOneFromCart.<string:id>")
def removeOneFromCart(id):
    try:
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('START TRANSACTION')

        try:
            cursor.execute('UPDATE Cart SET Amount = Amount - 1 WHERE CustomerID = %s and ProductID = %s', [session['id'], id])
            cursor.execute('DELETE FROM Cart WHERE Amount = 0')
        except:
            cursor.execute('ROLLBACK')

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
        return redirect(request.referrer)
    except:
        return redirect(url_for('home'))

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
            cursor.execute('INSERT INTO Reviews VALUES(NULL, %s, %s, %s, %s, %s, NULL)', [session['id'], id, comment, title, rating])

        mysql.connection.commit()
        return redirect(request.referrer)
    except:
        return redirect(url_for('home'))

@app.route("/deleteReview.<string:id>")
def deleteReview(id):
    try:
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('DELETE FROM Reviews WHERE CustomerID = %s and ProductID = %s', [session['id'], id])

        mysql.connection.commit()
        return redirect(request.referrer)
    except:
        return redirect(url_for('home'))

@app.route("/checkOut", methods=['GET', 'POST'])
def checkOut():
    if 'loggedin' in session:
        if request.method == 'POST' and 'country' in request.form and 'city' in request.form and 'zipCode' in request.form and 'address' in request.form:
            
            form = CheckOutForm()
            country = request.form['country']
            city = request.form['city']
            zipcode = request.form['zipCode']
            address = request.form['address']
            totalPrice = 0

            cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
            cursor.execute('START TRANSACTION')

            try:
                cursor.execute('INSERT INTO Orders VALUES(NULL, %s, %s, %s, %s, %s, %s) ', [session['id'], totalPrice, country, city, zipcode, address])
                OrderID = cursor.lastrowid

                cursor.execute('SELECT OrderID FROM Orders WHERE CustomerID = %s', [session['id']])
                orders = cursor.fetchall()
                cursor.execute('SELECT ProductID, Amount FROM Cart WHERE CustomerID = %s', [session['id']])
                cart = cursor.fetchall()

                #Check if enough in stock
                for row in cart:
                    cursor.execute('SELECT InStock, Price, ProductName, ProductPicture FROM Products WHERE ProductID = %s', [row['ProductID']])
                    data = cursor.fetchone()
                    if row["Amount"] > data["InStock"]:
                        flash(f'Sorry, but we dont have that many in stock')
                        return redirect(url_for('cart'))
                
                    #Calculate total price
                    cursor.execute('SELECT Price FROM Products WHERE ProductID = %s', [row['ProductID']])
                    price = cursor.fetchone()
                    totalPrice += row['Amount'] * data['Price']

                    #Updates in stock on different products
                    cursor.execute('UPDATE Products SET InStock = InStock - %s WHERE ProductID = %s', [row['Amount'], row['ProductID']])

                    #Insert OrderDetails
                    cursor.execute('INSERT INTO OrderDetails VALUES(NULL, %s, %s, %s)', [OrderID, row['ProductID'], row['Amount']])

                    #Insert into PurchaseHistory
                    cursor.execute('INSERT INTO PurchaseHistory VALUES(NULL, %s, %s, %s, %s, %s, NULL)', [session['id'], data['ProductName'], data['Price'], data['ProductPicture'], row['Amount']])

                #Update total price
                cursor.execute('UPDATE Orders SET TotalPrice = %s WHERE OrderID = %s', [totalPrice, OrderID])

                #Clears cart
                cursor.execute('DELETE FROM Cart WHERE CustomerID = %s', [session['id']])
            except:
                cursor.execute('ROLLBACK')
            
            mysql.connection.commit()
            flash(f'Purchase was successful, your products will arrive soon')

            return redirect(url_for('home'))
        return render_template('CheckOutPage.html')
    return redirect(url_for('login'))

if __name__ == "__main__":
    app.run(debug=True)
