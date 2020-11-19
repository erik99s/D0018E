from flask import Flask, redirect, url_for, render_template, flash, request
from forms import RegistrationForm, LoginForm
from flask_mysqldb import MySQLdb
import sys

app = Flask(__name__)

app.config['SECRET_KEY'] = '1c15e0b9ef383e18d6ba8646275b4c88'  

app.config['MYSQL_HOST'] = "localhost"
app.config['MYSQL_USER'] = "root"
app.config['MYSQL_PASSWORD'] = ""
app.config['MYSQL_DB'] = "user_db"

@app.route("/home")
def home():
    return render_template("HomePage.html")


@app.route("/register", methods=['GET', 'POST'])
def registrer():
    form = RegistrationForm()
    if form.validate_on_submit():
        flash(f'Account created for {form.email.data}!', 'success')
        return redirect(url_for('home'))
    print("fail", file=sys.stderr)
    return render_template('RegisterPage.html', title='Register', form=form)


@app.route("/login", methods=['GET', 'POST'])
def login():
    form = LoginForm()
    """
    if request.method == 'POST':
        cur = mySQL.connection.cursor()

        cur.execute("INSERT INTO users (form) VALUES (%s,%s)", (form))

        mySQL.connection.commit()

        cur.close()
        return "success"
    """
    return render_template('LoginPage.html', title='login', form=form)

@app.route("/loggedIn")
def loggedIn():
    render_template('LoggedInPage.html', title='loggedIn')

@app.route("/product")
def products():
    return render_template('ProductPage.html', title='product')

@app.route("/profile")
def profile():
    return render_template('ProfilePage.html', title='profile')

if __name__ == "__main__":
    app.run(debug=True)

