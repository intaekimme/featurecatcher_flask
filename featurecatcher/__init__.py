from flask import Flask
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
import os

db = SQLAlchemy()

# path that recorded video will be saved
savePath = str()

def user_setting():
    global savePath
    print("Specify the path to save the recorded video : ", end='')
    savePath = input()
    if savePath[-1] == '/':
        savePath = savePath[:-1]
    print("Recorded video will be saved in {path}".format(path=savePath))


def create_app():
    app = Flask(__name__)
    if not app.debug or os.environ.get("WERKZEUG_RUN_MAIN") == "true":
        user_setting()
    
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
