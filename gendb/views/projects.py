"""Projects view."""

from flask import Blueprint, redirect, url_for, render_template, g
from flask.ext.login import login_required, current_user

from gendb.extensions import db
from gendb.forms import AddProjectForm
from gendb.models import Project, groups

projects_bp = Blueprint('projects_bp', __name__)


@projects_bp.before_request
def before_request():
    g.user = current_user


@login_required
@projects_bp.route('/projects')
def projects():
    add_project = AddProjectForm()
    # projects = Project.query.join(groups, groups.c.project_id==Project.project_id)
    projects = g.user.project_member

    return render_template(
        '/projects/projects.html',
        projects=projects,
        title='Projects',
        add_project=add_project
    )


@login_required
@projects_bp.route('/add_project', methods=['POST'])
def add_project():
    form = AddProjectForm()

    if form.validate_on_submit():
        project = Project()

        # Create the project entry for the DB
        project.name = form.name.data
        project.description = form.description.data
        project.owner = g.user.email

        # Add and commit
        db.session.add(project)
        db.session.commit()

        # Insert in groups table
        ins = groups.insert().values(user_email=g.user.email, project_id=project.project_id)
        db.session.execute(ins)

        # Commit
        db.session.commit()

    return redirect(url_for('projects_bp.projects'))
