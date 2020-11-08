from flask import Flask, redirect, url_for, render_template, request

app = Flask(__name__)

@app.route("/")
def home():
    return render_template("HomePage.html")

@app.route("/login",methods=["POST", "GET"])
def login():
    return render_template("LoginPage.html")

#@app.route("/<usr>")
#def user(usr): 
#    return render_template()



#def shopping cart():



if __name__ == "__main__":
    app.run(debug=True)

