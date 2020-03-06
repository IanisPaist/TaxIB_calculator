from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager

# app = Flask(__name__) # to make the app run without any
app = Flask(__name__)
app.config['SECRET_KEY']='9f4524c7618dff15e241e048dd3449ab'
#config sqlite db
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'

#create db instanse
db = SQLAlchemy(app)
bcrypt = Bcrypt(app)
login_manager=LoginManager(app)

from application import routes