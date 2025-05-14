from datetime import datetime, timedelta, timezone
from flask import Blueprint, render_template, request, redirect, url_for, flash, session, g
from flask_login import current_user, LoginManager
from app.authentication.utils import login_required
from .forms import BudgetForm, GoalForm
from .models import User, Budget, Goal
from app.transactions.models import Transaction
from app import db

budgeting_and_goals_bp = Blueprint(
    'budgeting_and_goals', __name__, template_folder='templates', static_folder='static'
)


#Budgeting Helper Functions
def get_transactions_for_budget(user_id, category, period):
    now = datetime.now(timezone.utc)

    if period == 'weekly':
        start_date = (now - timedelta(days=now.weekday())).replace(hour=0, minute=0, second=0, microsecond=0)
    elif period == 'monthly':
        start_date = now.replace(day=1, hour=0, minute=0, second=0, microsecond=0)
    elif period == 'yearly':
        start_date = now.replace(month=1, day=1, hour=0, minute=0, second=0, microsecond=0)
    else:
        start_date = datetime(1, 1, 1, tzinfo=timezone.utc)

    transactions = Transaction.query.filter_by(
        user_id=user_id,
        category=category
    ).filter(
        Transaction.date >= start_date
    ).all()

    return transactions

def get_previous_transactions_for_budget(user_id, category, period):
    now = datetime.now(timezone.utc)

    if period == 'weekly':
        start = (now - timedelta(days=now.weekday() + 7)).replace(hour=0, minute=0, second=0, microsecond=0)
        end = start + timedelta(days=7)
    elif period == 'monthly':
        this_month_start = now.replace(day=1, hour=0, minute=0, second=0, microsecond=0)
        last_month_end = this_month_start - timedelta(seconds=1)
        start = last_month_end.replace(day=1, hour=0, minute=0, second=0, microsecond=0)
        end = last_month_end
    elif period == 'yearly':
        start = now.replace(year=now.year - 1, month=1, day=1, hour=0, minute=0, second=0, microsecond=0)
        end = now.replace(month=1, day=1, hour=0, minute=0, second=0, microsecond=0) - timedelta(seconds=1)
    else:
        return []

    transactions = Transaction.query.filter_by(
        user_id=user_id,
        category=category
    ).filter(
        Transaction.date >= start,
        Transaction.date <= end
    ).all()

    return transactions


# Budgeting
@budgeting_and_goals_bp.route('/budget', methods=['GET'])
@login_required
def view_budget():
    form = BudgetForm()
    user_id = session['user']['id']

    # Query the budgets created by the currently logged-in user
    user_budgets = Budget.query.filter_by(user_id=user_id).all()

    budget_summaries = []

    most_saved = None
    most_spent = None
    max_saved_pct = -1
    max_spent_pct = -1

    for budget in user_budgets:
        transactions = get_transactions_for_budget(user_id, budget.category, budget.period)
        expenses_total = sum(t.amount for t in transactions if t.transaction_type == 'expense')
        income_total = sum(t.amount for t in transactions if t.transaction_type == 'income')
        
        previous_transactions = get_previous_transactions_for_budget(user_id, budget.category, budget.period)
        previous_expenses = sum(t.amount for t in previous_transactions if t.transaction_type == 'expense')
        previous_income = sum(t.amount for t in previous_transactions if t.transaction_type == 'income')
        
        total_spent = expenses_total - income_total
        previous_total_spent = previous_expenses - previous_income
        
        # Prevent divide-by-zero
        if budget.limit and budget.limit > 0:
            saved_pct = max(0, (budget.limit - total_spent) / budget.limit)
            spent_pct = total_spent / budget.limit

            if saved_pct > max_saved_pct:
                max_saved_pct = saved_pct
                most_saved = budget

            if spent_pct > max_spent_pct:
                max_spent_pct = spent_pct
                most_spent = budget

        budget_summaries.append({
            'budget': budget,
            'transactions': transactions,
            'total_spent': total_spent,
            'previous_total_spent': previous_total_spent,
        })


    # Monthly income/spending
    now = datetime.now(timezone.utc)
    current_month = now.month
    current_year = now.year

    transactions = Transaction.query.filter_by(user_id=user_id).all()
    
    this_month_income = sum(t.amount for t in transactions if t.transaction_type == 'income' and t.date.month == current_month and t.date.year == current_year)
    this_month_expense = sum(t.amount for t in transactions if t.transaction_type == 'expense' and t.date.month == current_month and t.date.year == current_year)

    # Previous month (handle January case too)
    first_day_this_month = now.replace(day=1)
    last_day_previous_month = first_day_this_month - timedelta(days=1)
    previous_month = last_day_previous_month.month
    previous_year = last_day_previous_month.year
    
    last_month_income = sum(t.amount for t in transactions if t.transaction_type == 'income' and t.date.month == previous_month and t.date.year == previous_year)
    last_month_expense = sum(t.amount for t in transactions if t.transaction_type == 'expense' and t.date.month == previous_month and t.date.year == previous_year)
        
    return render_template('budgeting_and_goals/budget.html', form=form, summaries=budget_summaries,
        most_saved=most_saved, most_saved_pct=round(max_saved_pct * 100, 1) if most_saved else None,
        most_spent=most_spent, most_spent_pct=round(max_spent_pct * 100, 1) if most_spent else None,
        this_month_income=this_month_income, last_month_income=last_month_income,
        this_month_expense=this_month_expense, last_month_expense=last_month_expense)

@budgeting_and_goals_bp.route('/budget/edit/<int:id>', methods=['GET', 'POST'])
@login_required
def edit_budget(budget_id):
    budget = Budget.query.get_or_404(budget_id)

    # Ensure the user is the owner of the budget
    if budget.user_id != session['user']['id']:
        flash("You do not have permission to edit this budget.", "danger")
        return redirect(url_for('budgeting_and_goals.view_budget'))

    form = BudgetForm(obj=budget)  # Pre-fill the form with the current budget values

    if form.validate_on_submit():  # Save the changes when form is submitted
        # Update the budget with the new values from the form
        budget.category = form.category.data
        budget.limit = form.limit.data
        budget.period = form.period.data
        budget.description = form.description.data

        db.session.commit()  # Save to the database
        flash("Budget updated successfully!", "success")
        return redirect(url_for('budgeting_and_goals.view_budget'))  # Redirect after save

    return render_template('budgeting_and_goals/budget_edit.html', form=form, budget_id=id)

@budgeting_and_goals_bp.route('/budget/add', methods=['GET', 'POST'])
@login_required 
def add_budget():
    form = BudgetForm()  # Create a new form for adding a budget

    if form.validate_on_submit():  # Validate form data when submitted
        # Create a new Budget instance with form data
        new_budget = Budget(
            category=form.category.data,
            limit=form.limit.data,
            period=form.period.data,
            description=form.description.data,
            user_id=session['user']['id']
        )

        db.session.add(new_budget)  
        db.session.commit()  

        flash('Budget added successfully!', 'success') 
        return redirect(url_for('budgeting_and_goals.view_budget'))  # Redirect to view the budget list

    return render_template('budgeting_and_goals/budget_add.html', form=form)

@budgeting_and_goals_bp.route('/budget/delete/<int:id>', methods=['POST'])
@login_required
def delete_budget(budget_id):
    budget = Budget.query.get_or_404(budget_id)

    # Only allow deletion if the budget belongs to the current user
    if budget.user_id != session['user']['id']:
        flash("You are not authorized to delete this budget.", "danger")
        return redirect(url_for('budgeting_and_goals.view_budget'))

    db.session.delete(budget)
    db.session.commit()
    flash("Budget deleted successfully.", "success")

    # Redirect back to the budget overview page after deletion
    return redirect(url_for('budgeting_and_goals.view_budget'))

#Goal Helper Functions
def get_transactions_for_goal(user_id, start_date, deadline):
    """
    Fetch transactions for a given user between start_date and deadline.
    Separately totals expenses and income.
    """
    # Query all transactions in date range
    transactions = Transaction.query.filter_by(
        user_id = user_id,
    ).filter(
        Transaction.date >= datetime.combine(start_date, datetime.min.time(), tzinfo=timezone.utc),
        Transaction.date <= datetime.combine(deadline, datetime.max.time(), tzinfo=timezone.utc)
    ).all()

    return transactions

# Goals
@budgeting_and_goals_bp.route('/goals', methods=['GET'])
@login_required 
def view_goals():
    form = GoalForm()
    user_id = session['user']['id']
    user_goals = Goal.query.filter_by(user_id=user_id).all()

    goal_summaries = []
    total_goals = len(user_goals)
    completed_goals = 0

    for goal in user_goals:
        # Get transactions between goal start and deadline
        transactions = get_transactions_for_goal(user_id, goal.start_date, goal.deadline)
        expenses_total = sum(t.amount for t in transactions if t.transaction_type == 'expense')
        income_total = sum(t.amount for t in transactions if t.transaction_type == 'income')

        total_amount = goal.current_amount - expenses_total + income_total

        if total_amount >= goal.target_amount:
            completed_goals += 1

        goal_summaries.append({
            'goal': goal,
            'expenses_total': expenses_total,
            'income_total': income_total,
            'total_amount': total_amount,
            'transactions': transactions
        })

    in_progress = total_goals - completed_goals

    return render_template('budgeting_and_goals/goals.html', form=form, summaries=goal_summaries, 
                           total_goals=total_goals, completed_goals=completed_goals, in_progress=in_progress)

@budgeting_and_goals_bp.route('/goals/edit/<int:id>', methods=['GET', 'POST'])
@login_required 
def edit_goals(goal_id):
    goal = Goal.query.get_or_404(goal_id)

    # Ensure the user is the owner of the goal
    if goal.user_id != session['user']['id']:
        flash("You do not have permission to edit this goal.", "danger")
        return redirect(url_for('budgeting_and_goals.view_goals'))

    form = GoalForm(obj=goal)  # Pre-fill the form with the current goal values

    if form.validate_on_submit():  # Save the changes when form is submitted

        goal.title = form.title.data
        goal.target_amount = form.target_amount.data
        goal.current_amount = form.current_amount.data
        goal.start_date = form.start_date.data
        goal.deadline = form.deadline.data
        goal.description = form.description.data

        db.session.commit()
        flash("Goal updated successfully!", "success")
        return redirect(url_for('budgeting_and_goals.view_goals'))


    return render_template('budgeting_and_goals/goals_edit.html', form=form, goal_id=id)

@budgeting_and_goals_bp.route('/goals/add', methods=['GET', 'POST'])
@login_required
def add_goal():
    form = GoalForm()  # Create a new form for adding a goal

    if form.validate_on_submit():  # Validate form data when submitted

        new_goal = Goal(
            title=form.title.data,
            target_amount=form.target_amount.data,
            current_amount=form.current_amount.data,
            start_date=form.start_date.data,
            deadline=form.deadline.data,
            description=form.description.data,
            user_id=session['user']['id']
        )

        db.session.add(new_goal)
        db.session.commit()

        flash('Goal added successfully!', 'success')
        return redirect(url_for('budgeting_and_goals.view_goals'))  # Redirect to view the goals list

    return render_template('budgeting_and_goals/goals_add.html', form=form)

@budgeting_and_goals_bp.route('/goals/delete/<int:id>', methods=['POST'])
@login_required
def delete_goal(goal_id):
    goal = Goal.query.get_or_404(goal_id)

    if goal.user_id != session['user']['id']:
        flash("You are not authorized to delete this goal.", "danger")
        return redirect(url_for('budgeting_and_goals.view_goals'))

    db.session.delete(goal)
    db.session.commit()
    flash("Goal deleted successfully.", "success")
    return redirect(url_for('budgeting_and_goals.view_goals'))