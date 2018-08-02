from flask import Flask
from .config import configure, Database
from flask import Blueprint
from flask_restful import Api

config_env = 'test'

app = Flask(__name__, instance_relative_config=True)

print("hey")
configure(app, config_env)

print(Database.dbConnection('test'))
#db = SQLAlchemy(app)

#import models
print("heyyyy")
api_bp = Blueprint('api', __name__)
api = Api(api_bp)

#register blueprints
app.register_blueprint(api_bp, url_prefix="/api")

#initialize api routes
from .routes import init_routes
init_routes(api)
print("hey555")
from .db import db
db.init_app(app)

with app.app_context():
    db.create_all()