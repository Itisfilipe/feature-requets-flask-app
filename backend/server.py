import os

from routes import my_routes

from config import app_config
from flask import Flask
from flask_cors import CORS
from models import db


def create_app(config_name):
    app = Flask("app", instance_relative_config=True)
    app.register_blueprint(my_routes)
    app.config.from_object(app_config[config_name])
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    db.init_app(app)
    with app.app_context():
        db.create_all()
    cors = CORS()
    cors.init_app(app)
    return app


if __name__ == '__main__':
    config_name = os.getenv('APP_SETTINGS') or 'production'
    app = create_app(config_name)
    app.run()
