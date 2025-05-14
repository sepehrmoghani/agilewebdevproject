
from flask_wtf import FlaskForm
from wtforms import SubmitField
from wtforms.validators import DataRequired

class ShareForm(FlaskForm):
    submit = SubmitField('Update Share Settings')
