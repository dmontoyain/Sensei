import os
from . import dbConfig as Database
from flask_cors import CORS

def configure(app, configSetting):
    #   Configuration of application client_id as registered with 42
    #CLIENT_ID = os.environ.get("CLIENT_ID", default=None)
    #if not CLIENT_ID:
    #    return ValueError("No client id found for Sensei api")
    app.config['CLIENT_ID'] = '823adfcc4ef1759018f849376da1241c3546b2dd895d9f5bc7093649ed8cb187'

    #   Configuration of application secret as registered with 42
    #CLIENT_SECRET = os.environ.get("SECRET_KEY", default=None)
    #if not CLIENT_SECRET:
    #    return ValueError("No secret key found to configure Flask application.")
    app.config['CLIENT_SECRET'] = '9de9baec020f5a19789844fbaa0eaf1bdb4e8c6a0251e6be334da8d8214f4c81'
    
    #   dbConnection string used for communication with database
    app.config['SQLALCHEMY_DATABASE_URI'] = Database.dbConnection(configSetting)

    #   Additional app settings
    CORS(app)
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
