from flask import Blueprint, render_template, request, redirect, url_for, flash, session, g, current_app
from app.authentication import authentication_bp
from .forms import LoginForm, SignupForm, LoginInfo, UpdateProfileForm
from .models import User
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, Email, Optional, Length, EqualTo
import os
from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug.utils import secure_filename
from app import db

loginInfo = {}

@authentication_bp.before_request
def load_logged_in_user():
    user = session.get('user')
    if user:
        g.user = user
    else:
        g.user = None

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
                return redirect(url_for('dashboard.dashboard'))
            elif not user:
                flash("Email does not match any accounts", "danger")
            else:
                flash("Incorrect password", "danger")
    
    return render_template('authentication/login.html', form=form)


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
    return render_template('authentication/signup.html', form=form)

@authentication_bp.route('/profile')
def profile():
    user = session.get('user')
    if not user:
        return redirect(url_for('authentication.login'))
            
    return render_template('authentication/profile.html', user=user)

@authentication_bp.route('/profile/edit', methods=['GET', 'POST'])
def edit_profile():
    user_data = session.get('user')
    if not user_data:
        return redirect(url_for('authentication.login'))

    user = User.query.get(user_data['id'])
    form = UpdateProfileForm(obj=user)

    if form.validate_on_submit():
        user.first_name = form.first_name.data
        user.last_name = form.last_name.data
        user.email = form.email.data


        # Profile Picture
        pic_file = form.profile_pic.data
        if pic_file:
            filename = secure_filename(pic_file.filename)
            pic_path = os.path.join(current_app.config['UPLOAD_FOLDER'], filename)
            pic_file.save(pic_path)
            print("Saving to:", pic_path)
            user.profile_pic = filename
            print("Uploaded file:", pic_file, "Filename:", getattr(pic_file, 'filename', 'No filename'))
        
        # Password
        if form.current_password.data:
            if not check_password_hash(user.password, form.current_password.data):
                flash("Current password is incorrect.", "danger")
                return render_template('authentication/profile_edit.html', form=form, user=user)

            if not form.new_password.data:
                flash("New password cannot be empty.", "danger")
                return render_template('authentication/profile_edit.html', form=form, user=user)

            user.password = generate_password_hash(form.new_password.data)
            flash("Password updated successfully.", "success")
        else:
            flash("Profile updated successfully.", "success")

        db.session.commit()

        session['user'] = {
            'id': user.id,
            'first_name': user.first_name,
            'last_name': user.last_name,
            'email': user.email,
            'profile_pic': user.profile_pic if user.profile_pic else None
        }

        return redirect(url_for('authentication.profile'))

    return render_template('authentication/profile_edit.html', form=form, user=user)


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
