from flask import Blueprint, render_template, request, flash

authenciator = Blueprint('authenciator', __name__)

@authenciator.route('/login', methods=['GET', 'POST'])
def login():
    return render_template("login.html")

@authenciator.route('/logout')
def logout():
    return "<p>Logout</p>"

@authenciator.route('/register', methods=['GET', 'POST'])
def register():
    #get the type of user from "id" in register.html
    
    if request.method == 'POST':

        username = request.form.get('user1')
        password1 = request.form.get('password1')
        password2 = request.form.get('password2')
        
        if len(username) < 5:
            flash('Username must be greater than 5 characters.', category='error')
        elif password1 != password2:
            flash('Passwords do not match.', category='error')
        elif len(password1) < 5:
            flash('Password must be greater than 5 characters.', category='error')
        else:
            flash('Account creation successful', category='success')

    return render_template("register.html")

@authenciator.route('/form', methods=['GET','POST'])
def form():
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