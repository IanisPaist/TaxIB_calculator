from flask import Flask, render_template, url_for
from forms import RegistrationForm, LoginForm

# app = Flask(__name__) # to make the app run without any
app = Flask(__name__)
app.config['SECRET_KEY']='9f4524c7618dff15e241e048dd3449ab'

@app.route("/")
@app.route("/home")
def hello():
    return render_template("home.html")

@app.route("/login")
def login():
    form = LoginForm()
    return render_template("login.html", form = form)    

@app.route("/register")
def register():
    form = RegistrationForm()
    return render_template("register.html", form = form)    

@app.route("/about")
def about():
    return "About"

if __name__ == '__main__':
    app.run(debug=True)
