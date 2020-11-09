from flask import Flask, redirect, url_for, render_template #request
from flask import RegistrationForm, LoginForm

app = Flask(__name__)

app.config['SECRET_KEY'] = '1c15e0b9ef383e18d6ba8646275b4c88'  

@app.route("/")
def home():
    return render_template("HomePage.html")

@app.route("/register")
def registrer():
    form = RegistrationForm()
    return render_template('RegisterPage.html', title='Register', form=form)


@app.route("/login")
def login():
    form = LoginForm()
    return render_template('LoginPage.html', title='login', form=form)




if __name__ == "__main__":
    app.run(debug=True)

