from flask import Blueprint, render_template, request, flash, redirect, url_for
from .models import User
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_user, login_required, logout_user, current_user
from . import db  # database from __init__.py

authenciator = Blueprint('authenciator', __name__)


@authenciator.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')

        user = User.query.filter_by(username=username).first()
        if user:
            if check_password_hash(user.password, password):
                flash('Logged in Successfully!', category='success')
                login_user(user, remember=True)
                return redirect(url_for('viewer.home'))
            else:
                flash('Incorrect password, try again.', category='error')
        else:
            flash('Account does not exist.', category='error')

    return render_template("login.html", user=current_user)


@authenciator.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('authenciator.login'))


@authenciator.route('/register', methods=['GET', 'POST'])
def register():
    # get the type of user from "id" in register.html

    if request.method == 'POST':

        username = request.form.get('user1')
        password1 = request.form.get('password1')
        password2 = request.form.get('password2')

        user = User.query.filter_by(username=username).first()
        if user:
            flash('Username already exists.', category='error')
        elif len(username) < 5:
            flash('Username must be greater than 5 characters.', category='error')
        elif password1 != password2:
            flash('Passwords do not match.', category='error')
        elif len(password1) < 5:
            flash('Password must be greater than 5 characters.', category='error')
        else:
            new_user = User(username=username, password=generate_password_hash(
                password1, method='sha256'))
            db.session.add(new_user)
            db.session.commit()
            login_user(user, remember=True)
            flash('Account creation successful', category='success')
            return redirect(url_for('viewer.home'))

    return render_template("register.html", user=current_user)


@authenciator.route('/form', methods=['GET', 'POST'])
def form():
    if request.method == 'POST':
        numGallons = request.form.get('gallonsReq')
        date = request.form.get('deliveryDate')

        # address should not be inputed, should be retrived from client profile.
        # calculate suggest price with pricing module which will be imported later.
        # calculate total amount after pricing module.

        # catches an exception if user does not enter a valid number for numGallons.

        try:
            testVal = int(numGallons)
        except ValueError:
            flash('Number of gallons must me a valid integer', category='error')

    return render_template("form.html")


@authenciator.route('/complete', methods=['GET', 'POST'])
def completeReg():

    if request.method == 'POST':

        fullName = request.form.get('fullName')
        addr1 = request.form.get('address1')
        addr2 = request.form.get('address2')
        city = request.form.get('city')
        state = request.form.get('state-dropdown')
        zipcode = request.form.get('zipcode')

        if len(fullName) > 50:
            flash('Full Name cannot be longer than 50 characters', category='error')
        elif len(addr1) > 100:
            flash('Address 1 cannot be longer than 100 characters', category='error')
        elif len(addr2) > 100:
            flash('Address 2 cannot be longer than 100 characters', category='error')
        elif len(city) > 100:
            flash('City cannot be longer than 100 characters', category='error')
        elif len(zipcode) > 9:
            flash('Zipcode cannot be longer than 9 characters', category='error')
        elif len(zipcode) < 5:
            flash('Zipcode cannot be shorter than 5 characters', category='error')
        else:
            flash('Account creation successful', category='success')

        print("fullName:", fullName)
        print("addr1:", addr1)
        print("addr2:", addr2)
        print("city:", city)
        print("state:", state)
        print("zipcode:", zipcode)

    return render_template("completereg.html")
