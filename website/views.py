from flask import Blueprint, render_template, request
from flask_login import login_required, current_user

viewer = Blueprint('viewer', __name__)


@viewer.route('/')
def home():
    return render_template("home.html", user=current_user)


@viewer.route('/history')
@login_required
def history():
    return render_template("history.html", user=current_user)
