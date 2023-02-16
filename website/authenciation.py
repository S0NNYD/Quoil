from flask import Blueprint, render_template

authenciator = Blueprint('authenciator', __name__)

@authenciator.route('/login')
def login():
    return render_template("login.html")

@authenciator.route('/logout')
def logout():
    return "<p>Logout</p>"

@authenciator.route('/register')
def register():
    return render_template("register.html")