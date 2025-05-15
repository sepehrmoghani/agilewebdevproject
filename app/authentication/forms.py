from flask_wtf import FlaskForm
from flask_wtf.file import FileAllowed
from app import db
import re
from wtforms import StringField, PasswordField, SubmitField, FileField, ValidationError
from wtforms.validators import DataRequired, Email, Optional, Length, EqualTo

def pw_spaces(form, field):
    password = field.data
    if ' ' in password:
        raise ValidationError('Password cannot contain spaces.')

def pw_letter(form, field):
    password = field.data
    if not re.search(r'[A-Za-z]', password):
        raise ValidationError('Password must contain at least one letter.')

def pw_number(form, field):
    password = field.data
    if not re.search(r'\d', password):
        raise ValidationError('Password must contain at least one number.')

def pw_special(form, field):
    password = field.data
    if not re.search(r'[^A-Za-z0-9]', password):
        raise ValidationError('Password must contain at least one special character.')
    
class LoginInfo:
    def __init__(self, info):
        self.name = info.name
        self.email = info.email
        self.password = info.password

class LoginForm(FlaskForm):
    email = StringField('Email address', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Log in')

class SignupForm(FlaskForm):
    first_name = StringField('First Name', validators=[DataRequired()])
    last_name = StringField('Last Name', validators=[DataRequired()])
    email = StringField('Email address', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired(), Length(min=8, max=16), pw_spaces, pw_letter, pw_number, pw_special])
    repassword = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password', message='Passwords must match'), Length(min=8, max=16), pw_spaces, pw_letter, pw_number, pw_special])
    submit = SubmitField('Sign up')

class UpdateProfileForm(FlaskForm):
    first_name = StringField('First Name', validators=[DataRequired()])
    last_name = StringField('Last Name', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    profile_pic = FileField('Profile Picture', validators=[FileAllowed(['jpg', 'png'], 'Images only! Max file size: 5mb')])
    
    # Optional password change
    current_password = PasswordField('Current Password', validators=[Optional()])
    new_password = PasswordField('New Password', validators=[Optional(), Length(min=8, max=16), pw_spaces, pw_letter, pw_number, pw_special])
    confirm_password = PasswordField('Confirm New Password', validators=[
        Optional(), EqualTo('new_password', message='Passwords must match'), Length(min=8, max=16), pw_spaces, pw_letter, pw_number, pw_special
    ])

    submit = SubmitField('Update Profile')