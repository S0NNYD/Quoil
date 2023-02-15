from flask import Blueprint

viewer = Blueprint('viewer', __name__)

@viewer.route('/')
def home():
    return "<h1>Test</h1>"