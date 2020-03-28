import os
import secrets
import csv
from datetime import datetime, date
from flask import render_template, url_for, redirect, flash, request
from application.forms import RegistrationForm, LoginForm, UpdateAccountForm, DividendsUploadForm
from application.models import Users, Dividends
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

@app.route("/dividends", methods=["GET","POST"])
@login_required
def dividends():
    form = DividendsUploadForm()

    if form.validate_on_submit():

        #check that file exists
        if form.csv.data:
            
            # Create variable for uploaded file
            f = form.csv.data

            #store the file contents as a string
            fstring = f.read().decode("utf-8").lower()

            #everything is the file is separated by commas so to read we need to extract needed lines
            #they all start by DividendDetail and 17 words long
            
            #find boundaries of needed info
            index_left = fstring.find("DividendDetail".lower())
            index_right = fstring.find("DividendRevenueSummary".lower())

            #extract string
            tmp_string = fstring[index_left:index_right]

            #split by newline
            splitted_list = tmp_string.splitlines()
            
            #remove last ","
            splitted_list = [s.rstrip(",") for s in splitted_list]

            #creater a reader
            reader = csv.DictReader(splitted_list)

            for row in reader:
                if row["datadiscriminator"] == "summary":

                    #convert date
                    d1 = datetime.strptime(row["reportdate"], '%Y%m%d')
                    d2 = datetime.strftime(d1,"%d.%m.%Y")

                    exch_rate = 0
                    #get USD exchange rate
                    #open file and find rate
                    #if rate doenst exist on that date - take previous one
                    with open("application/usd.csv",'r') as file_usd:
                        usd_reader = csv.DictReader(file_usd)
                        while exch_rate == 0:
                            for d in usd_reader:
                                if datetime.strptime(d["data"],'%d.%m.%Y') == d1:
                                    exch_rate = float(d["curs"])
                                elif datetime.strptime(d["data"],'%d.%m.%Y') > d1:
                                    exch_rate = prev_exch_rate
                                else:
                                    prev_exch_rate = float(d["curs"])
                    
                    
                    #calculate income in rub
                    income_rub = float(row["grossinusd"])  * float(exch_rate)
                    
                    #Convert to Rub tax paid in USA
                    taxInUsRub = float(row["withholdinusd"]) * float(exch_rate)

                    #calculate rus tax
                    #1.forecast as 13%
                    tax13 = income_rub * -0.13
                    
                    #tax13 is max - calculate by how much tax paid in USA lower
                    taxInRus = tax13 - taxInUsRub
                    if taxInRus > 0:
                        taxInRus = 0

                    #calculate net income USD
                    net_usd = float(row["grossinusd"]) - float(row["withholdinusd"])

                    #calculate net income in RUB
                    net_rub = income_rub - taxInUsRub - taxInRus

                    # add info into database
                    data = Dividends(
                        symbol = row["symbol"].upper(),
                        div_date = d2,
                        div_year = int(row["reportdate"][0:4]),
                        gross_income_usd = float(row["grossinusd"]),
                        tax_us = float(row["withholdinusd"]),
                        exchange_rate = "{:.2f}".format(exch_rate),
                        gross_income_rub = "{:.2f}".format(income_rub),
                        tax_USA_rub = "{:.2f}".format(taxInUsRub),
                        tax_RUS_rub = "{:.2f}".format(taxInRus),
                        net_income_usd = "{:.2f}".format(net_usd),
                        net_income_rub = "{:.2f}".format(net_rub),
                        users_id = current_user.id
                    )
                    

                    #add changes to db
                    db.session.add(data)
                    db.session.commit()

        #redirect to this page as GET request to show data
        return redirect(url_for('dividends')) 
    else:
        
        #show all current data in db
        
        #query db to get all values
        q = Dividends.query.filter(Dividends.users_id == current_user.id).order_by(Dividends.div_year.desc()).all()

        #query db to get summary for db

        q2 = db.session.query(

                        Dividends.div_year, 
                        db.func.sum(Dividends.gross_income_usd),
                        db.func.sum(Dividends.tax_us),
                        db.func.sum(Dividends.gross_income_rub),
                        db.func.sum(Dividends.tax_USA_rub),
                        db.func.sum(Dividends.tax_RUS_rub),
                        db.func.sum(Dividends.net_income_usd),
                        db.func.sum(Dividends.net_income_rub)
                        ).group_by(Dividends.div_year).order_by(Dividends.div_year.desc()).all()

        
        #q2 = db.session.query(Dividends.div_year, db.func.sum(Dividends.gross_income_usd),db.func.sum(Dividends.tax_us),db.func.sum(Dividends.gross_income_rub),db.func.sum(Dividends.tax_USA_rub),db.func.sum(Dividends.tax_RUS_rub),db.func.sum(Dividends.net_income_usd),db.func.sum(Dividends.net_income_rub)).group_by(Dividends.div_year).all()

        #query returns list of lists but we will covert it to list of dicts
        #iterate row by row
        i = 0
        summary = []
        for row in q2:
            summary.append(
                {
                "div_year": row[0],
                "gross_income_usd": "{:.2f}".format(row[1]),
                "tax_us": "{:.2f}".format(row[2]),
                "gross_income_rub": "{:.2f}".format(row[3]),
                "tax_USA_rub": "{:.2f}".format(row[4]),
                "tax_RUS_rub": "{:.2f}".format(row[5]),
                "net_income_usd": "{:.2f}".format(row[6]),
                "net_income_rub": "{:.2f}".format(row[7])
                }
            )
            i += 1

        #render template
        return render_template("dividends.html", form=form, dividends=q, summary=summary)   

@app.route("/account", methods=["GET","POST"])
@login_required
def account():
    form = UpdateAccountForm()

    if form.validate_on_submit():

        #update values for current user
        current_user.username = form.username.data
        current_user.email = form.email.data

        #commit them to database
        db.session.commit()

        #flash success message
        flash('Your account have been updated', 'success')
        
        #return to account page without POST request
        return redirect(url_for('account'))

    elif request.method == "GET":
        form.username.data = current_user.username
        form.email.data = current_user.email

    return render_template("account.html", form=form)    



@app.route("/dividends_delete", methods=["GET","POST"])
@login_required
def delete_dividends_data():

    #query db for current user data 
    result = Dividends.query.filter(Dividends.users_id == current_user.id).all()

    #delete
    for r in result:
        db.session.delete(r)
    db.session.commit()

    return redirect(url_for('dividends'))
