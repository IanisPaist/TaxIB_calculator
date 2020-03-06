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

