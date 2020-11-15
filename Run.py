from flask import Flask, redirect, url_for, render_template, flash, redirect
from forms import RegistrationForm, LoginForm
import sys

#run
app = Flask(__name__)

app.config['SECRET_KEY'] = '1c15e0b9ef383e18d6ba8646275b4c88'  

@app.route("/")
@app.route("/home")
def home():
    return render_template("HomePage.html")


@app.route("/register", methods=['GET', 'POST'])
def registrer():
    form = RegistrationForm()
    if form.validate_on_submit():
        flash(f'Account created for{form.email.data}!', 'success')
        return redirect(url_for('home'))
    print("fail", file=sys.stderr)
    return render_template('RegisterPage.html', title='Register', form=form)


@app.route("/login")
def login():
    form = LoginForm()
    return render_template('LoginPage.html', title='login', form=form)

@app.route("/products")
def products():
    return render_template('ProductsPage.html', title='products')

@app.route("/profile")
def profile():
    form = ProfileForm()
    return render_template('ProfilePage.html', title='profile', form=form)

if __name__ == "__main__":
    app.run(debug=True)

