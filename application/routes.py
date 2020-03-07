from flask import render_template, url_for, redirect, flash, request
from application.forms import RegistrationForm, LoginForm
from application.models import Users, History
from application import app, db, bcrypt
from flask_login import login_user, current_user, logout_user, login_required

@app.route("/home")
@app.route("/")
@login_required
def home():
    return render_template("home.html")

@app.route("/login", methods=["GET","POST"])
def login():

    #if current user is already logged in -> redirect to home page
    if current_user.is_authenticated:
        return redirect(url_for('home'))

    #assign a form class imported from forms.py
    form = LoginForm()

    if form.validate_on_submit():
    
        #check if users email exists in db, None if not
        user = Users.query.filter_by(email=form.email.data).first()

        #check that user exists and password is correct
        if user and bcrypt.check_password_hash(user.password, form.password.data):

            #log in that user 
            login_user(user, remember=form.remember.data)
            
            #redirect to home page
            return redirect(url_for('home'))

        else:
            #flash message if login unsuccessful
            flash('Invalid login or password', 'danger')

    return render_template("login.html", form = form)    

@app.route("/register", methods=["GET","POST"])
def register():

    #if current user is already logged in -> redirect to home page
    if current_user.is_authenticated:
        return redirect(url_for('home'))

    #assign a form class imported from forms.py
    form = RegistrationForm()

    #validate form data and send flash message if sucessfully created
    #first - message , second - category to then use for bootstrap styling
    if form.validate_on_submit():

        #hash password
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')

        #create a new user
        user = Users(username=form.username.data, email=form.email.data, password=hashed_password)

        #add change to db
        db.session.add(user)

        #commit change to db
        db.session.commit()

        #show message that a user can now login
        flash("account created! you can log in now", "success")

        #redirect to login page
        return redirect(url_for('login'))

    return render_template("register.html", form = form)    

@app.route("/logout")
def logout():
    logout_user()
    return redirect(url_for('login'))

@app.route("/history")
@login_required
def history():
    return render_template("history.html")    

@app.route("/account")
@login_required
def account():
    return render_template("account.html")    