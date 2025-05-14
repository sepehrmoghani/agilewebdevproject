from datetime import datetime, timezone
from flask_wtf import FlaskForm
from wtforms import StringField, SelectField, SubmitField, RadioField, TextAreaField
from wtforms.validators import InputRequired, Length, ValidationError
from wtforms.fields import FloatField
from wtforms import DateField

def two_decimal_places(form, field):
    if round(field.data, 2) != field.data:
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
    limit = FloatField("Limit", validators=[InputRequired(), two_decimal_places], render_kw={"placeholder": "e.g. 200.00"})
    period = SelectField("Period", choices=[('weekly', 'Weekly'), ('monthly', 'Monthly'), ('yearly', 'Yearly')], validators=[InputRequired()])
    description = TextAreaField("Description (Optional)")
    submit = SubmitField("Save Budget")


class GoalForm(FlaskForm):
    title = StringField("Title", validators=[InputRequired(), Length(max=60)], render_kw={"placeholder": "Untitled"})
    target_amount = FloatField("Target Amount", validators=[InputRequired(), two_decimal_places], render_kw={"placeholder": "e.g. 1000.00"})
    current_amount = FloatField("Current Amount", validators=[InputRequired(), two_decimal_places], render_kw={"placeholder": "e.g. 250.00"})
    start_date = DateField("Start Date", format='%Y-%m-%d', validators=[InputRequired()], render_kw={"placeholder": "YYYY-MM-DD"})
    deadline = DateField("Deadline", validators=[InputRequired()], format='%Y-%m-%d', render_kw={"placeholder": "YYYY-MM-DD"})
    description = TextAreaField("Description (Optional)")
    submit = SubmitField("Set Goal")
    
    # Custom validation for the start date
    def validate_start_date(self, field):
        current_date = datetime.now(timezone.utc).date()
        if field.data < current_date:
            raise ValidationError("Start date cannot be in the past.")
        if self.deadline.data and field.data >= self.deadline.data:
            raise ValidationError("Start date must be before the deadline.")