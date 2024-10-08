from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_cors import CORS
from urllib.parse import quote
from flasgger import Swagger

app = Flask(__name__)

# Secret keys and database configuration
app.secret_key = '*(&*(@*&(*@(^!(*@75876528378932^@%*&^(*@*@&#*'
app.config["SQLALCHEMY_DATABASE_URI"] = (
    f"mysql+pymysql://dev_app:%s@116.109.193.21:3307/app-trading?charset=utf8mb4"
) % quote("dev@1234")
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False  # Best to turn off to save memory
app.config['SECRET_KEY'] = '38a5f73c-ff0f-4b81-b466-701071019a4d'

# Initialize extensions
db = SQLAlchemy(app)
login = LoginManager(app)

CORS(app, resources={r"/*": {"origins": "*"}})


print("Success")

swagger_template = {
    "info": {
        "title": "Trading API",
        "description": "API documentation for the Trading application",
        "version": "1.0.0"
    },
    "host": "localhost:5000",
    "basePath": "/",
    "schemes": ["http", "https"]
}
swagger_config = {
    "headers": [],
    "specs": [
        {
            "endpoint": 'apispec_1',
            "route": '/apispec_1.json',
            "rule_filter": lambda rule: True,  # Include all routes
            "model_filter": lambda tag: True,  # Include all models
        }
    ],
    "static_url_path": "/flasgger_static",
    "swagger_ui": True,
    "specs_route": "/swagger/"
}
Swagger(app, template=swagger_template, config=swagger_config)


