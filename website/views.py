from flask import Blueprint, render_template

viewer = Blueprint('viewer', __name__)

@viewer.route('/')
def home():
    return render_template("home.html")