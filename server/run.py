from flask import Flask
from config.settings import configure
from flask import Blueprint
from flask_restful import Api
from resources import init_routes, globalOnlineUsers

config_env = 'test'

def create_app(config_env):
    app = Flask(__name__)

    configure(app, config_env)

    #   starting url address for every endpoint
    api_bp = Blueprint('api', __name__)
    api = Api(api_bp)
    app.register_blueprint(api_bp, url_prefix="/api")

    init_routes(api)

    from models import db
    db.init_app(app)

    globalOnlineUsers.run()
    return app

if __name__ == '__main__':
    app = create_app('test')
    app.run(debug=True, use_reloader=False)