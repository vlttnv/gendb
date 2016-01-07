"""Projects view."""

from flask import Blueprint, redirect, url_for, render_template, g, flash
from flask.ext.login import login_required

from sqlalchemy.sql import and_
from sqlalchemy.orm.exc import NoResultFound

from gendb.extensions import db
from gendb.forms import AddProjectForm, AddProjectContributorForm
from gendb.models import Project, groups, User

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

    print(project.contributors)

    return render_template(
        '/projects/project.html',
        title='Project Name',
        project=project,
        add_contrib=AddProjectContributorForm(project_id=project_id)
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


@projects_bp.route('/add_contributor', methods=['POST'])
@login_required
def add_contributor():
    form = AddProjectContributorForm()

    if form.validate_on_submit():
        try:
            u = User.query.filter_by(email=form.email.data).one()
        except NoResultFound:
            flash('This user email does not exist.', 'danger')
            return redirect(url_for(
                'projects_bp.project',
                project_id=form.project_id.data
            ))

        # Insert in groups table
        ins = groups.insert().values(
            user_email=u.email,
            project_id=form.project_id.data
        )
        db.session.execute(ins)

        db.session.commit()

        flash('Contributor added successfuly', 'success')
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


@projects_bp.route('/delete_contributor/<int:project_id>/<contrib_id>')
@login_required
def delete_contributor(project_id, contrib_id):
    try:
        project = Project.query.filter_by(project_id=project_id).one()
    except NoResultFound:
        flash('Project does not exist.', 'danger')
        return redirect(url_for('projects_bp.projects'))

    if g.user.email != project.owner or g.user.email == project.owner:
        flash('Action not allowed.', 'danger')
        return redirect(url_for('projects_bp.projects'))

    db.session.execute(groups.delete().where(and_(
        groups.c.user_email == contrib_id,
        groups.c.project_id == project_id
    )))
    db.session.commit()

    flash('Contributor removed from project.', 'success')
    return redirect(url_for('projects_bp.project', project_id=project_id))
