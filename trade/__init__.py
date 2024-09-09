from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_cors import CORS
from urllib.parse import quote
from dotenv import load_dotenv
import os

load_dotenv()

# user_name = os.getenv('USER')
# password = os.getenv('PASSWORD')
# host = os.getenv('HOST')
# db = os.getenv('DBNAME')
# port_db = os.getenv('DB_PORT')

app = Flask(__name__)
app.secret_key = '*(&*(@*&(*@(^!(*@75876528378932^@%*&^(*@*@&#*'
app.config["SQLALCHEMY_DATABASE_URI"] = (
    f"mysql+pymysql://dev_app:%s@116.108.91.115:3307/app-trading?charset=utf8mb4") % quote("dev@1234")
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = True
app.config['SECRET_KEY'] = '38a5f73c-ff0f-4b81-b466-701071019a4d'

# Initialize CORS
CORS(app, resources={r"/*": {"origins": "*"}})  # Allow all origins, adjust as needed

db = SQLAlchemy(app)
login = LoginManager(app)



if __name__ == '__main__':
    app.run(debug=True)
