"""GenDB app init."""

from flask import Flask, redirect, url_for, g, session

from gendb.extensions import db, lm
from gendb.models import User
from gendb.views.engine import engine_bp
from gendb.views.home import home_bp
from gendb.views.projects import projects_bp


def create_app():
    gendb_app = Flask(__name__, instance_relative_config=True)

    gendb_app.config.from_object('config')
    gendb_app.config.from_pyfile('config.py')

    config_blueprints(gendb_app)
    config_extensions(gendb_app)
    config_befores(gendb_app)

    lm_decorators()

    return gendb_app


def config_blueprints(the_app):
    the_app.register_blueprint(home_bp)
    the_app.register_blueprint(projects_bp)
    the_app.register_blueprint(engine_bp)


def config_extensions(the_app):
    db.init_app(the_app)
    lm.init_app(the_app)
    # oid.init_app(the_app)
    # rds.init_app(the_app)
    return


def lm_decorators():
    @lm.user_loader
    def load_user(id):
        return User.query.get(int(id))

    @lm.unauthorized_handler
    def unauthorized():
        # TODO: flash
        return redirect(url_for('home_bp.login'))


def config_befores(the_app):
    @the_app.before_request
    def before_request():
        """
        A handler before every request. TODO: More.
        """

        if 'user_id' in session:
            g.user = User.query.filter_by(id=session['user_id']).first()
        else:
            g.user = None
