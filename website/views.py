from flask import Blueprint, render_template

viewer = Blueprint('viewer', __name__)

@viewer.route('/')
def home():
    return render_template("home.html")

@viewer.route('/history')
def history():
    return render_template("history.html")