from . import dbConfig as Database
from flask_cors import CORS

def configure(app, configSetting):
    CORS(app)
    app.config['SQLALCHEMY_DATABASE_URI'] = Database.dbConnection(configSetting)
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
