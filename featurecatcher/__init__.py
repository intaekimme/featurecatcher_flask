from flask import Flask
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
import os

db = SQLAlchemy()

# path that recorded video will be saved
savePath = os.path.dirname(__file__) + '/static/temp/videos'

def create_app():
    app = Flask(__name__)
    app.config.from_envvar('APP_CONFIG_FILE')

    # ORM
    db.init_app(app)
    app.app_context().push()
    from . import models

    # blueprint
    from .views import main_views, list_views
    app.register_blueprint(main_views.bp)
    app.register_blueprint(list_views.bp)

    return app
