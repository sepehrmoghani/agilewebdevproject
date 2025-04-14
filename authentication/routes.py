from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from authentication import auth_bp
from .forms import LoginForm
from .forms import SignupForm
from app.models import LoginInfo

loginInfo = {}

@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    
    if request.method == 'POST':
        if form.validate_on_submit():
            email = request.form['email']
            password = request.form['password']
            user = loginInfo.get(email)
            if user and user['password'] == password:
                session['user'] = user  # save user info to session
                return redirect(url_for('auth.profile'))
            elif email not in loginInfo:
                flash("Email does not match any accounts", "danger")
                return redirect(url_for('auth.login'))
            elif user['password'] != password:
                flash("Incorrect password", "danger")
                return redirect(url_for('auth.login'))
    
    return render_template('login.html', form=form, loginInfo=loginInfo)

@auth_bp.route('/signup', methods=['GET', 'POST'])
def signup():
    form = SignupForm()
    if form.validate_on_submit():
        if form.email.data in loginInfo:
            flash("Email already registered. Please log in.", "warning")
            return redirect(url_for('auth.login'))
        name = form.name.data
        email = form.email.data
        password = form.password.data
        # Store the new user in the fake database
        loginInfo[email] = {'name': name, 'email': email, 'password': password}
        flash("Registration successful! Please log in.", "success")
        return redirect(url_for('auth.login'))
    return render_template('signup.html', form=form)

@auth_bp.route('/profile')
def profile():
    user = session.get('user')
    if not user:
        return redirect(url_for('auth.login'))
            
    return render_template('profile.html', user=user, loginInfo=loginInfo)

@auth_bp.route('/logout')
def logout():
    session.pop('user', None)
    return redirect(url_for('auth.logout_message')) 

@auth_bp.route('/logout_message')
def logout_message():
    flash("You have been logged out successfully.", "success")
    return redirect(url_for('auth.login')) 
    

@auth_bp.route('/privacy')
def privacy():
    return render_template('privacy.html')

@auth_bp.route('/feedback')
def feedback():
    return render_template('feedback.html')

@auth_bp.route('/index')
def index():
    return render_template('index.html')
