from flask import Blueprint, render_template, request, flash, redirect, url_for
from .models import User, FuelQuote, Userlogin
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_user, login_required, logout_user, current_user
from . import db  # database from __init__.py
from datetime import datetime

authenciator = Blueprint('authenciator', __name__)


@authenciator.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')

        user = Userlogin.query.filter_by(username=username).first()
        if user:
            if check_password_hash(user.password, password):
                login_user(user, remember=True)
                if user.firstTime == True:
                    flash('Please complete your registration', category='success')
                    return redirect(url_for('authenciator.completeReg'))
                else:
                    flash('Login Successful!', category='success')
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
        

        username = request.form.get('username')
        password1 = request.form.get('password1')
        password2 = request.form.get('password2')

   
        user = Userlogin.query.filter_by(username=username).first()
        if user: 
            flash('Username already exists.', category='error')
        elif len(username) < 5:
            flash('Username must be atleast 5 characters.', category='error')
        elif password1 != password2:
            flash('Passwords do not match.', category='error')
        elif len(password1) < 5:
            flash('Password must be atleast 5 characters.', category='error')
        else:
            new_user = Userlogin(username=username, password=generate_password_hash(
                password1, method='sha256'), firstTime = True)
            db.session.add(new_user)
            db.session.commit()
            flash('Account creation successful', category='success')
            return redirect(url_for('authenciator.login'))

    return render_template("register.html", user=current_user)


@authenciator.route('/form', methods=['GET', 'POST'])
@login_required
def form():
    if current_user.firstTime == True:
        flash('Please complete your registration', category='error')
        return redirect(url_for('authenciator.completeReg'))
    if request.method == 'POST':
        gallons_req = request.form.get('gallons_req')
        delivery_date = request.form.get('delivery_date')
        suggested_price = request.form.get('suggested_price')
        total_amount = request.form.get('total_amount')


        
        if gallons_req.isdigit() != True:
            flash('Number of gallons must be a valid integer', category='error')
        else:
            new_quote_form = FuelQuote(
                gallons_req=gallons_req, delivery_address1=current_user.userInfo.address, delivery_address2=current_user.userInfo.address2,
                delivery_state=current_user.userInfo.state, delivery_city=current_user.userInfo.city, delivery_zipcode=current_user.userInfo.zipcode, delivery_date=delivery_date,
                suggested_price=suggested_price, total_amount=total_amount, user_id=current_user.id)
            db.session.add(new_quote_form)
            db.session.commit()
            flash("Quote Requested!", category='success')
            return redirect(url_for('viewer.history'))

        

    return render_template("form.html", user=current_user)


@authenciator.route('/complete', methods=['GET', 'POST'])
def completeReg():

    if request.method == 'POST':

        fullName = request.form.get('fullname')
        addr1 = request.form.get('address1')
        addr2 = request.form.get('address2')
        city = request.form.get('city')
        state = request.form.get('statedropdown')
        zipcode = request.form.get('zipcode')

        

        if len(fullName) > 50:
            flash('Full Name cannot be longer than 50 characters',
                  category='error')
        elif len(addr1) > 100:
            flash('Address 1 cannot be longer than 100 characters',
                  category='error')
        elif len(addr2) > 100:
            flash('Address 2 cannot be longer than 100 characters',
                  category='error')
        elif len(city) > 100:
            flash('City cannot be longer than 100 characters', category='error')
        elif len(zipcode) > 9:
            flash('Zipcode cannot be longer than 9 characters', category='error')
        elif len(zipcode) < 5:
            flash('Zipcode cannot be shorter than 5 characters', category='error')
        else:
            newUser = User(
                fullname = fullName, address = addr1, address2 = addr2,
                city = city, state = state, zipcode = zipcode, loginId = current_user.id
            )
            current_user.firstTime = False
            db.session.add(newUser)
            db.session.commit()
            flash('Account creation successful', category='success')
            return redirect(url_for('viewer.home'))
    

    return render_template("completereg.html", user = current_user)