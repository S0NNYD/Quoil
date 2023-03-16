from flask import Blueprint, render_template, request, jsonify, flash, redirect, url_for
from flask_login import login_required, current_user
from .models import FuelQuote, User, Userlogin
from . import db  # database from __init__.py
import json


viewer = Blueprint('viewer', __name__)


@viewer.route('/')
def home():
    return render_template("home.html", user=current_user)


@viewer.route('/history', methods=['GET', 'POST'])
@login_required
def history():
    return render_template("history.html", user=current_user)


@viewer.route('/delete-quote', methods=['POST'])
def delete_quote():
    quote = json.loads(request.data)
    print(quote)
    quote_no = quote['quote_no']
    quote = FuelQuote.query.get(quote_no)
    if (quote):
        if quote.user_id == current_user.id:
            db.session.delete(quote)
            db.session.commit()
            return jsonify({})
