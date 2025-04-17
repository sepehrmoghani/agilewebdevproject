from flask_wtf import FlaskForm
from wtforms import StringField, SelectField, SubmitField
from wtforms.validators import InputRequired, Length, ValidationError
from wtforms.fields import FloatField
from wtforms import DateField

def two_decimal_places(form, field):
    if round(field.data, 2) != field.data:
        raise ValidationError("Value must have at most 2 decimal places.")

class BudgetForm(FlaskForm):
    category = StringField("Category", validators=[InputRequired(), Length(max=50)], render_kw={"placeholder": "e.g. Groceries"})
    limit = FloatField("Limit", validators=[InputRequired(), two_decimal_places], render_kw={"placeholder": "e.g. 200.00"})
    period = SelectField("Period", choices=[('weekly', 'Weekly'), ('monthly', 'Monthly'), ('yearly', 'Yearly')], validators=[InputRequired()])
    submit = SubmitField("Save Budget")

class GoalForm(FlaskForm):
    title = StringField("Title", validators=[InputRequired(), Length(max=100)], render_kw={"placeholder": "Untitled"})
    target_amount = FloatField("Target Amount", validators=[InputRequired(), two_decimal_places], render_kw={"placeholder": "e.g. 1000.00"})
    current_amount = FloatField("Current Amount", validators=[InputRequired(), two_decimal_places], render_kw={"placeholder": "e.g. 250.00"})
    deadline = DateField("Deadline", validators=[InputRequired()], format='%Y-%m-%d', render_kw={"placeholder": "YYYY-MM-DD"})
    submit = SubmitField("Set Goal")