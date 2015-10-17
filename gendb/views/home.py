"""Home view."""

from flask import Blueprint, render_template


home_bp = Blueprint('home_bp', __name__)


@home_bp.route('/')
def index():
    return render_template('/home/index.html')


@home_bp.route('/register', methods=['GET', 'POST'])
def register():
    return render_template('/home/register.html')
