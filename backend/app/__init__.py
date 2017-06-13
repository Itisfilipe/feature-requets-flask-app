from flask_api import FlaskAPI

from .routes import my_routes
from .models import db
from config import app_config


def create_app(config_name):
    app = FlaskAPI(__name__, instance_relative_config=True)
    app.register_blueprint(my_routes)
    app.config.from_object(app_config[config_name])
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    # init db
    db.init_app(app)
    with app.app_context():
        db.create_all()

    return app