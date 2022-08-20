from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate


# setup DB
db = SQLAlchemy()


def create_app(**config_overrides):
    app = Flask(__name__)

    # load config
    app.config.from_pyfile("settings.py")

    # apply overrides for tests
    app.config.update(config_overrides)

    # initialize DB
    db.init_app(app)
    Migrate(app, db)

    # import blueprints
    ...

    # register blueprints
    ...

    return app
