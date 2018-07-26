import config.dbConfig as Database
import pymysql

def configure(app, configSetting):
    app.config['SQLALCHEMY_DATABASE_URI'] = Database.dbConnection('test')
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True

# 42 App Api Keys
class apikeys:
    uid = ''
    secret = ''