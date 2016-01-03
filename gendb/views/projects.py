"""Projects view."""

from flask import Blueprint, redirect, url_for, render_template, g, flash
from flask.ext.login import login_required

from gendb.extensions import db
from gendb.forms import AddProjectForm, AddProjectContributerForm
from gendb.models import Project, groups, User
from sqlalchemy.orm.exc import NoResultFound

projects_bp = Blueprint('projects_bp', __name__)


@projects_bp.route('/projects')
@login_required
def projects():
    """List all projects the user is a member of."""

    add_project = AddProjectForm()
    projects = g.user.project_member

    return render_template(
        '/projects/projects.html',
        projects=projects,
        title='Projects',
        add_project=add_project
    )


@projects_bp.route('/project/<int:project_id>')
@login_required
def project(project_id):
    """Single project page."""

    try:
        project = Project.query.filter_by(project_id=project_id).one()
    except NoResultFound:
        flash('This project does not exist.', 'warning')
        return redirect(url_for('projects_bp.projects'))

    print(project.contributers)

    return render_template(
        '/projects/project.html',
        title='Project Name',
        project=project,
        add_contrib=AddProjectContributerForm(project_id=project_id)
    )


@projects_bp.route('/add_project', methods=['POST'])
@login_required
def add_project():
    """Add a new project."""

    form = AddProjectForm()

    if form.validate_on_submit():
        project = Project()

        # Create the project entry for the DB
        project.name = form.name.data
        project.description = form.description.data
        project.owner = g.user.email

        db.session.add(project)
        db.session.commit()

        # Insert in groups table
        ins = groups.insert().values(
            user_email=g.user.email,
            project_id=project.project_id
        )
        db.session.execute(ins)

        db.session.commit()
    else:
        flash('Incomplete form. Please fill all the fields.', 'warning')
        return redirect(url_for('projects_bp.projects'))

    return redirect(url_for(
        'projects_bp.project',
        project_id=project.project_id)
    )


@projects_bp.route('/delete/<int:project_id>')
@login_required
def delete_project(project_id):
    """Delete a project and all associated data."""

    try:
        project = Project.query.filter_by(project_id=project_id).one()
    except NoResultFound:
        flash('This project does not exist.', 'warning')
        return redirect(url_for('projects_bp.projects'))

    db.session.delete(project)
    db.session.commit()

    flash('Project successfuly deleted.', 'success')
    return redirect(url_for('projects_bp.projects'))


@projects_bp.route('/add_contributer', methods=['POST'])
@login_required
def add_contributer():
    form = AddProjectContributerForm()

    if form.validate_on_submit():
        try:
            User.query.filter_by(email=form.email.data).one()
        except NoResultFound:
            flash('This user email does not exist.', 'danger')
            return redirect(url_for(
                'projects_bp.project',
                project_id=form.project_id.data
            ))

        # Insert in groups table
        ins = groups.insert().values(
            user_email=g.user.email,
            project_id=form.project_id.data
        )
        db.session.execute(ins)

        db.session.commit()

        flash('Contributer added successfuly', 'success')
    else:
        flash('Incomplete form. Please fill all the fields.', 'warning')
        return redirect(url_for(
            'projects_bp.project',
            project_id=form.project_id.data)
        )

    return redirect(url_for(
        'projects_bp.project',
        project_id=form.project_id.data)
    )
