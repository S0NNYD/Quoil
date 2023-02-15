from flask import Blueprint

authenciator = Blueprint('authenciator', __name__)

@authenciator.route('/login')
def login():
    return "<p>Login</p>"

@authenciator.route('/logout')
def logout():
    return "<p>Logout</p>"

@authenciator.route('/register')
def register():
    return "<p>Register</p>"