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
        print(request.form)
    return render_template("register.html")

@authenciator.route('/form', methods=['GET','POST'])
def form():
    return render_template("form.html")

@authenciator.route('/complete', methods=['GET', 'POST'])
def completeReg():
    return render_template("completereg.html")