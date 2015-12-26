"""Home view."""

from hashlib import sha1

from flask import Blueprint, render_template, redirect, url_for, flash, g
from flask.ext.login import (
    login_required, login_user, logout_user
)
from sqlalchemy.orm.exc import NoResultFound

from gendb.extensions import db
from gendb.forms import RegisterForm, LoginForm
from gendb.models import User

home_bp = Blueprint('home_bp', __name__)


@home_bp.route('/')
@login_required
def index():
    return render_template(
        '/home/index.html',
        title='Overview'
    )


@home_bp.route('/register', methods=['GET', 'POST'])
def register():
    """Render register form and handle registration."""

    form = RegisterForm()

    if form.validate_on_submit():
        u = User()
        u.email = form.email.data
        u.password = sha1(form.pw1.data.encode('utf-8')).hexdigest()

        db.session.add(u)
        db.session.commit()

        login_user(u)

        return redirect(url_for('home_bp.index'))
    return render_template('/home/register.html', form=form)


@home_bp.route('/login', methods=['GET', 'POST'])
def login():
    """Render login form and login user."""

    if g.user is not None and g.user.is_authenticated:
        return redirect(url_for('home_bp.index'))

    form = LoginForm()

    if form.validate_on_submit():
        try:
            u = User.query.filter_by(email=form.email.data).one()
            password = sha1(form.pw1.data.encode('utf-8')).hexdigest()
            if u.password == password:
                login_user(u)
                return redirect(url_for('home_bp.index'))
            else:
                flash('Incorrect username or password', 'danger')
                return redirect(url_for('home_bp.login'))

        except NoResultFound:
            flash('User not found.', 'danger')
            return redirect(url_for('home_bp.login'))

    return render_template('/home/login.html', form=form)


@home_bp.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('home_bp.login'))
