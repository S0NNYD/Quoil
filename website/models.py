from . import db  # database from __init__.py
from flask_login import UserMixin
from sqlalchemy.sql import func


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    fullname = db.Column(db.String(50))
    address = db.Column(db.String(100))
    address2 = db.Column(db.String(100))
    city = db.Column(db.String(100))
    state = db.Column(db.String(2))
    zipcode = db.Column(db.String(5))
    quotes = db.relationship('FuelQuote')
    loginId = db.Column(db.Integer, db.ForeignKey('userlogin.id'))
    userlogin = db.relationship('Userlogin', backref='user', uselist=False)

    def get_first_time(self):
        if self.userlogin:
            return self.userlogin.firstTime
        else:
            return None


class Userlogin(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(150), unique=True)
    password = db.Column(db.String(150))
    firstTime = db.Column(db.Boolean)
    



class FuelQuote(db.Model):
    quote_no = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    gallons_req = db.Column(db.Integer)
    delivery_date = db.Column(db.String(11))
    delivery_address1 = db.Column(db.String(100))
    delivery_address2 = db.Column(db.String(100))
    delivery_city = db.Column(db.String(100))
    delivery_state = db.Column(db.String(2))
    delivery_zipcode = db.Column(db.Integer)
    suggested_price = db.Column(db.Integer)
    total_amount = db.Column(db.Integer)
