from flask import Flask, redirect, url_for, render_template, flash, redirect
from forms import RegistrationForm, LoginForm

#run program

app = Flask(__name__)

app.config['SECRET_KEY'] = '1c15e0b9ef383e18d6ba8646275b4c88'  

@app.route("/")
def home():
    return render_template("HomePage.html")


@app.route("/register", methods=['GET', 'POST'])
def registrer():
    form = RegistrationForm()
    if form.validate_on_submit():
        flash(f'Account created for{form.username.data}!','success')
        return redirect(url_for('HomePage.html'))
    return render_template('RegisterPage.html', title='Register', form=form)


@app.route("/login")
def login():
    form = LoginForm()
    return render_template('LoginPage.html', title='login', form=form)

@app.route("/products")
def products():
    return render_template('ProductsPage.html', title='products')

if __name__ == "__main__":
    app.run(debug=True)

