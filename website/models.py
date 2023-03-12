from . import db #database from __init__.py
from flask_login import UserMixin
from sqlalchemy.sql import func

class User(db.model, UserMixin):
    id = db.column(db.Integer, primary_key=True)
    username = db.Column(db.String(150), unique=True)
    password = db.Column(db.String(150))


class User_info(db.model):
    id = db.column(db.Integer, primary_key=True)
    fullName = db.Column(db.String(50))
    Address1 = db.Column(db.String(100))
    Address2 = db.Column(db.String(100))
    City = db.Column(db.String(100))
    State = db.Column(db.String(2))
    Zip = db.Column(db.String(9))

class Fuel_Quote(db.model):
    id = db.column(db.Integer, primary_key=True)
    gallons_req = db.Column(db.Integer(150))
    delivery_date = db.Column(db.DateTime(timezone=True), default=func.now())
    delivery_state = db.Column(db.String(100))
    delivery_address = db.Column(db.String(100))
    suggested_price = db.Column(db.Integer(150))
    total_amount = db.Column(db.Integer(150))




    
