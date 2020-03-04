from flask import Flask, render_template, url_for, redirect
#in forms.py created two classes of forms
from forms import RegistrationForm, LoginForm
from flask import flash
#import sqlalchemy
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

# app = Flask(__name__) # to make the app run without any
app = Flask(__name__)
app.config['SECRET_KEY']='9f4524c7618dff15e241e048dd3449ab'
#config sqlite db
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'

#create db instanse
db = SQLAlchemy(app)


#create SQL table for user info with name users (lowercase)
class Users(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(120),unique=True, nullable=False)
    password = db.Column(db.String(60),nullable=False)
    cash_balance = db.Column(db.Integer,nullable=False, default = 10000)
    transactions  = db.relationship("History", backref="current_user", lazy=True) #relationship with history by its foreign key

    #define how object looks when we print it out
    def __repr__(self):
        return f"User('{self.username}', '{ self.email}', '{self.cash_balance}')"

#create SQL table for transaction history
class History(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    ticker = db.Column(db.String(100), nullable = False)
    tr_date = db.Column(db.DateTime, nullable = False, default=datetime.utcnow)
    users_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)

    def __repr__(self):
        return f"History('{self.ticker}','{self.users_id}')"


@app.route("/home")
def home():
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

    #validate form data and send flash message if sucessfully created
    #first - message , second - category to then use for bootstrap styling
    if form.validate_on_submit():
        flash("account created!", "success")
        return redirect("/")

    return render_template("register.html", form = form)    

@app.route("/about")
def about():
    return "About"

if __name__ == '__main__':
    app.run(debug=True)
