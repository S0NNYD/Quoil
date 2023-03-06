from . import db #database from __init__.py
from flask_login import UserMixin

class User(db.model, UserMixin):
    id = db.column(db.Integer, primary_key=True)
    username = db.Column(db.String(150), unique=True)
    password = db.Column(db.String(150))
    fullName = db.Column(db.String(50))
    Address1 = db.Column(db.String(100))
    Address2 = db.Column(db.String(100))
    City = db.Column(db.String(100))
    State = db.Column(db.String(2))
    Zip = db.Column(db.String(9))



    
