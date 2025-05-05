from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from app.authentication import authentication_bp
from .forms import LoginForm, SignupForm, User, LoginInfo
from werkzeug.security import generate_password_hash
from werkzeug.security import check_password_hash
from app import db

loginInfo = {}

@authentication_bp.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    
    if request.method == 'POST':
        if form.validate_on_submit():
            email = form.email.data
            password = form.password.data
            
            # Query the user from the database
            user = User.query.filter_by(email=email).first()
            if user and check_password_hash(user.password, password):
                session['user'] = {
                    'id': user.id,
                    'first_name': user.first_name,
                    'last_name': user.last_name,
                    'email': user.email
                }
                flash("Logged in successfully!", "success")
                return redirect(url_for('authentication.profile'))
            elif not user:
                flash("Email does not match any accounts", "danger")
            else:
                flash("Incorrect password", "danger")
    
    return render_template('login.html', form=form)


@authentication_bp.route('/signup', methods=['GET', 'POST'])
def signup():
    form = SignupForm()
    if form.validate_on_submit():
        # Check if the email is already registered
        existing_user = User.query.filter_by(email=form.email.data).first()
        if existing_user:
            flash("Email already registered. Please log in.", "warning")
            return redirect(url_for('authentication.login'))
        
        # Create a new user and save to the database
        hashed_password = generate_password_hash(form.password.data)
        new_user = User(
            first_name=form.first_name.data,
            last_name=form.last_name.data,
            email=form.email.data,
            password=hashed_password
        )
        db.session.add(new_user)
        db.session.commit()
        
        flash("Registration successful! Please log in.", "success")
        return redirect(url_for('authentication.login'))
    return render_template('signup.html', form=form)

@authentication_bp.route('/profile')
def profile():
    user = session.get('user')
    if not user:
        return redirect(url_for('authentication.login'))
            
    return render_template('profile.html', user=user)

@authentication_bp.route('/logout')
def logout():
    session.pop('user', None)
    return redirect(url_for('authentication.logout_message')) 

@authentication_bp.route('/logout_message')
def logout_message():
    flash("You have been logged out successfully.", "success")
    return redirect(url_for('authentication.login')) 

@authentication_bp.route('/delete_account', methods=['POST'])
def delete_account():
    user = session.get('user')
    if not user:
        flash("You need to log in to delete your account.", "warning")
        return redirect(url_for('authentication.login'))

    # Query the user from the database
    user_to_delete = User.query.get(user['id'])
    if user_to_delete:
        db.session.delete(user_to_delete)
        db.session.commit()
        session.pop('user', None)  # Log the user out
        flash("Your account has been deleted successfully.", "success")
        return redirect(url_for('authentication.login'))
    else:
        flash("Account not found.", "danger")
        return redirect(url_for('authentication.profile'))
    

@authentication_bp.route('/privacy')
def privacy():
    return render_template('privacy.html')

@authentication_bp.route('/feedback')
def feedback():
    return render_template('feedback.html')

@authentication_bp.route('/index')
def index():
    return render_template('index.html')
