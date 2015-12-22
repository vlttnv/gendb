"""Projects view."""

from flask import Blueprint, render_template
from flask.ext.login import login_required

from gendb.extensions import db

projects_bp = Blueprint('projects_bp', __name__)


@login_required
@projects_bp.route('/projects')
def projects():
    return render_template('/projects/projects.html')
