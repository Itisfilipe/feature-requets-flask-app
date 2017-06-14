import os

try:
    from .app import create_app
except:
    from app import create_app

config_name = os.getenv('APP_SETTINGS') or "development"
app = create_app(config_name)

if __name__ == '__main__':
    app.run()
