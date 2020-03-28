from application import db, login_manager
from flask_login import UserMixin
from datetime import datetime


#
@login_manager.user_loader
def load_user(user_id):
    return Users.query.get(int(user_id))


#create SQL table for user info with name users (lowercase)
class Users(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(120),unique=True, nullable=False)
    password = db.Column(db.String(60),nullable=False)
    dividends  = db.relationship("Dividends", backref="current_user", lazy=True) #relationship with Dividends by its foreign key

    #define how object looks when we print it out
    def __repr__(self):
        return f"User('{self.username}', '{ self.email}', '{self.cash_balance}')"

#create SQL table for dividends history
class Dividends(db.Model, UserMixin):
    dividend_id = db.Column(db.Integer, primary_key=True)
    symbol = db.Column(db.String(100), nullable = False)
    div_date = db.Column(db.String(50), nullable = False)
    div_year = db.Column(db.Integer, nullable = False)
    gross_income_usd = db.Column(db.Float,nullable = False)
    tax_us = db.Column(db.Float,nullable=False)
    exchange_rate = db.Column(db.Float,nullable=False)
    gross_income_rub = db.Column(db.Float,nullable = False)
    tax_USA_rub = db.Column(db.Float,nullable=False)
    tax_RUS_rub = db.Column(db.Float,nullable=False)
    net_income_usd = db.Column(db.Float,nullable=False)
    net_income_rub = db.Column(db.Float,nullable=False)
    users_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)

    def __repr__(self):
        return f"Dividends('{self.symbol}','{self.users_id}')"

