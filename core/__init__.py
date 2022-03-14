from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from decouple import config
from flask_restful import Api, Resource, reqparse

app = Flask(__name__)
api = Api(app)
app.config.from_object(config("APP_SETTINGS"))

db = SQLAlchemy(app)
migrate = Migrate(app, db)

# from core import routes
