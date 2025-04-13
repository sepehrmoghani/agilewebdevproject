from flask import Blueprint, render_template, request, redirect, url_for
from authentication import auth_bp
from .forms import LoginForm
from .forms import SignupForm

@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    return render_template('login.html', form=form)
    #if form.validate_on_submit():
        # Do login logic here
        #email = form.email.data
        #password = form.password.data
        # Example: check credentials, redirect, flash message, etc.
        #flash("Logged in successfully!", "success")
        #return redirect(url_for('auth.profile'))  # Or wherever

    #return render_template('login.html', form=form)

@auth_bp.route('/signup')
def signup():
    form = SignupForm()
    return render_template('signup.html', form=form)

@auth_bp.route('/privacy')
def privacy():
    return render_template('privacy.html')

@auth_bp.route('/feedback')
def feedback():
    return render_template('feedback.html')

@auth_bp.route('/index')
def index():
    return render_template('index.html')
