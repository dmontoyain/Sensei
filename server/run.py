from flask import Flask
from config.settings import configure

def create_app(config_env):
    app = Flask(__name__)

    configure(app, config_env)

    #   starting url address for every endpoint
    from app import api_bp
    app.register_blueprint(api_bp, url_prefix="/api")

    from models import db
    db.init_app(app)
    return app

if __name__ == '__main__':
    app = create_app("test")
    app.run(debug=True)