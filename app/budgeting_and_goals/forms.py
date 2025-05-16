from datetime import datetime, timezone, date
from flask_wtf import FlaskForm
from wtforms import StringField, SelectField, SubmitField, HiddenField, TextAreaField
from wtforms.validators import InputRequired, Length, ValidationError
from wtforms.fields import FloatField
from wtforms import DateField

def positive_num(form, field):
    if field.data is None:
        return
    try:
        value = float(field.data)
    except (TypeError, ValueError):
        return
    if value <= 0:
        raise ValidationError("Value must be a positive number.")

def two_decimal_places(form, field):
    if field.data is None:
        return
    try:
        value = float(field.data)
    except (TypeError, ValueError):
        raise ValidationError("Value must be a number.")
    if round(value, 2) != value:
        raise ValidationError("Value must have at most 2 decimal places.")

class BudgetForm(FlaskForm):
    category = SelectField("Category", 
        choices=[
            ('', 'Choose a Category'),
            ('Childcare', 'Childcare'),
            ('Eating out & takeaway', 'Eating out & takeaway'),
            ('Education', 'Education'),
            ('Entertainment', 'Entertainment'),
            ('Fees & interest', 'Fees & interest'),
            ('Gifts & donations', 'Gifts & donations'),
            ('Groceries', 'Groceries'),
            ('Health & medical', 'Health & medical'),
            ('Home', 'Home'),
            ('Home loan', 'Home loan'),
            ('Insurance', 'Insurance'),
            ('Personal care', 'Personal care'),
            ('Pets', 'Pets'),
            ('Professional services', 'Professional services'),
            ('Shopping', 'Shopping'),
            ('Sport & fitness', 'Sport & fitness'),
            ('Super contribution', 'Super contribution'),
            ('Tax paid', 'Tax paid'),
            ('Travel & holidays', 'Travel & holidays'),
            ('Uncategorised', 'Uncategorised'),
            ('Utilities', 'Utilities'),
            ('Vehicle & transport', 'Vehicle & transport')],
        validators=[InputRequired()],
        coerce=str
    )
    limit = FloatField("Limit", validators=[InputRequired(), positive_num, two_decimal_places], render_kw={"placeholder": "e.g. 200.00"})
    period = SelectField("Period", choices=[('', 'Choose a Period'), ('weekly', 'Weekly'), ('monthly', 'Monthly'), ('yearly', 'Yearly')], validators=[InputRequired()])
    description = TextAreaField("Description (Optional)")
    submit = SubmitField("Save Budget")

def validate_start_date(form, field):
    if field.data > date.today():
        raise ValidationError("Start date cannot be in the future.")

def current_limit(form, field):
    if field.data is None:
        return
    try:
        target = float(form.target_amount.data)
        current = float(field.data)
        if current > target:
            raise ValidationError("Current amount cannot exceed target amount.")
    except (TypeError, ValueError):
        return

def validate_deadline(self, field):
    if field.data <= date.today():
        raise ValidationError("Deadline must be a future date.")

class GoalForm(FlaskForm):
    title = StringField("Title", validators=[InputRequired(), Length(max=60)], render_kw={"placeholder": "Untitled"})
    target_amount = FloatField("Target Amount", validators=[InputRequired(), positive_num, two_decimal_places], render_kw={"placeholder": "e.g. 1000.00"})
    current_amount = FloatField("Current Amount", validators=[InputRequired(), current_limit, two_decimal_places], render_kw={"placeholder": "e.g. 250.00"})
    salary_amount = FloatField("Salary Amount", validators=[InputRequired(), positive_num, two_decimal_places], render_kw={"placeholder": "e.g. 2000.00"})
    salary_frequency = SelectField("Salary Frequency", 
        choices=[
            ('weekly', 'Weekly'),
            ('fortnightly', 'Fortnightly'),
            ('monthly', 'Monthly'),
            ('annually', 'Annually')
        ],
        validators=[InputRequired()]
    )
    salary_percentage = FloatField("Salary Percentage", render_kw={"readonly": True})
    start_date = DateField("Start Date", format='%Y-%m-%d', default=datetime.now(timezone.utc).date(), validators=[InputRequired(), validate_start_date], render_kw={"placeholder": "YYYY-MM-DD"})
    original_start_date = HiddenField()
    deadline = DateField("Deadline", validators=[InputRequired(), validate_deadline], format='%Y-%m-%d', render_kw={"placeholder": "YYYY-MM-DD"})
    description = TextAreaField("Description (Optional)")
    submit = SubmitField("Set Goal")