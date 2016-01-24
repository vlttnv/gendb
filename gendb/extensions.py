"""Initialize extensions."""

from flask.ext.login import LoginManager
from flask.ext.sqlalchemy import SQLAlchemy


db = SQLAlchemy()
lm = LoginManager()
