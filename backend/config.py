class Config(object):
    """Parent configuration class."""
    SQLALCHEMY_DATABASE_URI = 'sqlite:///./db.sqlite3'
    CSRF_ENABLED = True


class DevelopmentConfig(Config):
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///./db_dev.sqlite3'


class TestingConfig(Config):
    """Configurations for Testing, with a separate test database."""
    TESTING = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///./db_test.sqlite3'
    DEBUG = True
    LIVESERVER_PORT=8943


class ProductionConfig(Config):
    """Configurations for Production."""
    DEBUG = False
    TESTING = False


app_config = {
    'development': DevelopmentConfig,
    'testing': TestingConfig,
    'production': ProductionConfig,
}
