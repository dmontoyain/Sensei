from flask import Flask
from .config import configure, Database
from flask import Blueprint
from flask_restful import Api

#	Edit this to choose environment
config_env = 'test'

app = Flask(__name__)

configure(app, config_env)

#	Import models
api_bp = Blueprint('api', __name__)
api = Api(api_bp)

#	Register blueprints
app.register_blueprint(api_bp, url_prefix="/api")

#	Initialize API routes
from .routes import init_routes
init_routes(api)

from .db import db
db.init_app(app)
