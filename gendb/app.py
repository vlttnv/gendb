"""GenDB app init."""

from flask import Flask

from gendb.extensions import db
from .views.home import home_bp


def create_app():
    gendb_app = Flask(__name__, instance_relative_config=True)

    gendb_app.config.from_object('config')
    gendb_app.config.from_pyfile('config.py')

    config_blueprints(gendb_app)
    config_extensions(gendb_app)

    return gendb_app


def config_blueprints(the_app):
    the_app.register_blueprint(home_bp)


def config_extensions(the_app):
    db.init_app(the_app)
    # lm.init_app(the_app)
    # oid.init_app(the_app)
    # rds.init_app(the_app)
    return
