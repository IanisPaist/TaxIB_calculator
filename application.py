from flask import Flask, render_template, url_for, redirect
#in forms.py created two classes of forms
from forms import RegistrationForm, LoginForm
from flask import flash

# app = Flask(__name__) # to make the app run without any
app = Flask(__name__)
app.config['SECRET_KEY']='9f4524c7618dff15e241e048dd3449ab'

@app.route("/")
@app.route("/home")
def hello():
    return render_template("home.html")

@app.route("/login")
def login():
    #assign a form class imported from forms.py
    form = LoginForm()
    return render_template("login.html", form = form)    

@app.route("/register", methods=["GET","POST"])
def register():
    #assign a form class imported from forms.py
    form = RegistrationForm()

    #validate form data
    
    #redirect to home page

    return render_template("register.html", form = form)    

@app.route("/about")
def about():
    return "About"

if __name__ == '__main__':
    app.run(debug=True)
