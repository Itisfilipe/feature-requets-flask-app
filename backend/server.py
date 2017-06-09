import os
from flask import Flask
from config.config import app_config
from model import db
from routes import my_routes


def create_app(config_name):
    app = Flask("app", instance_relative_config=True)
    app.register_blueprint(my_routes)
    app.config.from_object(app_config[config_name])
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    db.init_app(app)
    with app.app_context():
        db.create_all()
    return app


if __name__ == '__main__':
    config_name = os.getenv('APP_SETTINGS') or 'production'
    app = create_app(config_name)
    app.run()
