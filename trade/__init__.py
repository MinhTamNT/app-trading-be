from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from urllib.parse import quote
from flask_login import LoginManager
app = Flask(__name__)
app.secret_key = '*(&*(@*&(*@(^!(*@75876528378932^@%*&^(*@*@&#*'
app.config["SQLALCHEMY_DATABASE_URI"] = "mysql+pymysql://root:%s@localhost/trade?charset=utf8mb4" % quote('120900')
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = True
app.config['SECRET_KEY'] = '38a5f73c-ff0f-4b81-b466-701071019a4d'
db = SQLAlchemy(app)
login = LoginManager(app)