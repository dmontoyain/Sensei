import config.dbConfig as Database
import pymysql

def configure(app, configSetting):
    app.config['SQLALCHEMY_DATABASE_URI'] = Database.dbConnection(configSetting)
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True

# 42 App Api Keys
class apikeys:
    uid = '3cc82d2287f91eb882a29c47bd8671597085b0c89cd434715e30df0a1d86cb4c'
    secret = 'bf56d9c3726fe99388ec712fdbc20843d30eeb5b6bcb797d16c1fb58b24961ac'
    