from . import db  # database from __init__.py
from flask_login import UserMixin
from sqlalchemy.sql import func


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(150), unique=True)
    password = db.Column(db.String(150))
    # fullName = db.Column(db.String(50))
    # Address1 = db.Column(db.String(100))
    # Address2 = db.Column(db.String(100))
    # City = db.Column(db.String(100))
    # State = db.Column(db.String(2))
    # Zip = db.Column(db.String(9))
    # quotes = db.relationship('Fuel_Quote')


class User_login(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(150), unique=True)
    password = db.Column(db.String(150))


class Fuel_Quote(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    gallons_req = db.Column(db.Integer)
    delivery_date = db.Column(db.DateTime(timezone=True), default=func.now())
    delivery_address1 = db.Column(db.String(100))
    delivery_address2 = db.Column(db.String(100))
    delivery_city = db.Column(db.String(100))
    delivery_state = db.Column(db.String(2))
    delivery_zipcode = db.Column(db.Integer)
    suggested_price = db.Column(db.Integer)
    total_amount = db.Column(db.Integer)
