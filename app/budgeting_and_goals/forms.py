from datetime import datetime, timezone
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
            ('Business', 'Business'),
            ('Cash', 'Cash'),
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
            ('Other investments', 'Other investments'),
            ('Personal care', 'Personal care'),
            ('Pets', 'Pets'),
            ('Professional services', 'Professional services'),
            ('Shares', 'Shares'),
            ('Shopping', 'Shopping'),
            ('Sport & fitness', 'Sport & fitness'),
            ('Super contribution', 'Super contribution'),
            ('Tax paid', 'Tax paid'),
            ('Transfer & payments', 'Transfer & payments'),
            ('Travel & holidays', 'Travel & holidays'),
            ('Uncategorised', 'Uncategorised'),
            ('Utilities', 'Utilities'),
            ('Vehicle & transport', 'Vehicle & transport'),
            ('Wages and Income','Wages and Income')],
        validators=[InputRequired()],
        coerce=str
    )
    limit = FloatField("Limit", validators=[InputRequired(), positive_num, two_decimal_places], render_kw={"placeholder": "e.g. 200.00"})
    period = SelectField("Period", choices=[('', 'Choose a Period'), ('weekly', 'Weekly'), ('monthly', 'Monthly'), ('yearly', 'Yearly')], validators=[InputRequired()])
    description = TextAreaField("Description (Optional)")
    submit = SubmitField("Save Budget")

def current_limit(form, field):
    if field.data is None or form.target_amount.data is None:
        return 
    try:
        current = float(field.data)
        target = float(form.target_amount.data)
    except (TypeError, ValueError):
        return
    if current > target:
        raise ValidationError("Current amount cannot exceed the target amount.")

def validate_start_date(self, field):
    current_date = datetime.now(timezone.utc).date()
    original_date_raw = self.original_start_date.data

    # Convert original_start_date if it exists
    original_start_date = None
    if original_date_raw:
        try:
            original_start_date = datetime.strptime(original_date_raw, "%Y-%m-%d").date()
        except ValueError:
            raise ValidationError("Invalid original start date format.")

    # Validation rules
    if original_start_date:
        if field.data < original_start_date:
            raise ValidationError("Cannot move date earlier than the current start date.")
    elif field.data < current_date:
        raise ValidationError("Start date cannot be in the past.")

    if self.deadline.data and field.data >= self.deadline.data:
        raise ValidationError("Start date must be before the deadline.")
        
def validate_deadline(self, field):
    if self.start_date.data and field.data <= self.start_date.data:
        raise ValidationError("Deadline must be after the start date.")

class GoalForm(FlaskForm):
    title = StringField("Title", validators=[InputRequired(), Length(max=60)], render_kw={"placeholder": "Untitled"})
    target_amount = FloatField("Target Amount", validators=[InputRequired(), positive_num, two_decimal_places], render_kw={"placeholder": "e.g. 1000.00"})
    current_amount = FloatField("Current Amount", validators=[InputRequired(), current_limit, two_decimal_places], render_kw={"placeholder": "e.g. 250.00"})
    start_date = DateField("Start Date", format='%Y-%m-%d', default=datetime.now(timezone.utc).date(), validators=[InputRequired(), validate_start_date], render_kw={"placeholder": "YYYY-MM-DD"})
    original_start_date = HiddenField()
    deadline = DateField("Deadline", validators=[InputRequired(), validate_deadline], format='%Y-%m-%d', render_kw={"placeholder": "YYYY-MM-DD"})
    description = TextAreaField("Description (Optional)")
    submit = SubmitField("Set Goal")