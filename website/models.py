from . import db #database from __init__.py
from flask_login import UserMixin

class User(db.model, UserMixin):
    id = db.column(db.Integer, primary_key=True)
    username = db.Column(db.String(150), unique=True)
    password = db.Column(db.String(150))