from flask import Flask
from .config import configure, Database
from flask import Blueprint
from flask_restful import Api
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow

#	Edit this to choose environment
app = Flask(__name__)

configure(app, 'test')

db = SQLAlchemy(app)
ma = Marshmallow(app)
#	Import models

api_bp = Blueprint('api', __name__)
api = Api(api_bp)

#	Register blueprints
app.register_blueprint(api_bp, url_prefix="/api")

#	Initialize API routes
from .routes import init_routes
init_routes(api)
