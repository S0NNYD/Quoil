from flask import Blueprint, render_template
from flask_login import login_required, current_user

viewer = Blueprint('viewer', __name__)


@viewer.route('/')
def home():
    return render_template("home.html")


@viewer.route('/history')
def history():
    return render_template("history.html")


@viewer.route('/form')
@login_required
def createForm():
    return render_template("form.html")
