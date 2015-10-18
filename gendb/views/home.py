"""Home view."""

from hashlib import sha1

from flask import Blueprint, render_template, redirect, url_for
from flask.ext.login import login_required, login_user, logout_user

from gendb.extensions import db
from gendb.forms import RegisterForm
from gendb.models import User

home_bp = Blueprint('home_bp', __name__)


@home_bp.route('/')
@login_required
def index():
    return render_template('/home/index.html')


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
