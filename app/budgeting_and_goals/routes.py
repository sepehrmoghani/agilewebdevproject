from datetime import datetime, timedelta, timezone
from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from sqlalchemy.exc import SQLAlchemyError
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

@budgeting_and_goals_bp.route('/budget/edit/<int:budget_id>', methods=['GET', 'POST'])
@login_required
def edit_budget(budget_id):
    budget = Budget.query.get_or_404(budget_id)

    if budget.user_id != session['user']['id']:
        return redirect(url_for('budgeting_and_goals.view_budget', error='not_authorized_budget'))


    form = BudgetForm(obj=budget)

    if form.validate_on_submit():
        budget.category = form.category.data
        budget.limit = form.limit.data
        budget.period = form.period.data
        budget.description = form.description.data

        db.session.commit()
        
        return redirect(url_for('budgeting_and_goals.view_budget', success='budget_edited'))
    else:
        print("Form errors:", form.errors)

    return render_template('budgeting_and_goals/budget_edit.html', form=form, budget_id=budget_id)

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

        return redirect(url_for('budgeting_and_goals.view_budget', success='budget_added'))
    else:
        print("Form errors:", form.errors)

    return render_template('budgeting_and_goals/budget_add.html', form=form)

@budgeting_and_goals_bp.route('/budget/delete/<int:budget_id>', methods=['POST'])
@login_required
def delete_budget(budget_id):
    budget = Budget.query.get_or_404(budget_id)

    # Only allow deletion if the budget belongs to the current user
    if budget.user_id != session['user']['id']:
        return redirect(url_for('budgeting_and_goals.view_budget', error='not_authorized_budget'))


    db.session.delete(budget)
    db.session.commit()

    return redirect(url_for('budgeting_and_goals.view_budget', success='budget_deleted'))

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

@budgeting_and_goals_bp.route('/goals', methods=['GET'])
@login_required 
def view_goals():
    form = GoalForm()
    user_id = session['user']['id']

    show_hidden = request.args.get('show_hidden', 'false').lower() == 'true'

    if show_hidden:
        user_goals = Goal.query.filter_by(user_id=user_id).all()  # All goals including hidden
    else:
        user_goals = Goal.query.filter_by(user_id=user_id, is_hidden=False).all()  # Only visible goals

    hidden_goals = [g for g in user_goals if g.is_hidden] if show_hidden else []

    goal_summaries = []
    all_goals = Goal.query.filter_by(user_id=user_id).all()  # All goals, regardless of hidden
    total_goals = len(all_goals)
    completed_goals = len([g for g in all_goals if g.date_completed is not None])

    for goal in user_goals:
        transactions = get_transactions_for_goal(user_id, goal.start_date, goal.deadline)
        expenses_total = sum(t.amount for t in transactions if t.transaction_type == 'expense')
        income_total = sum(t.amount for t in transactions if t.transaction_type == 'income')

        total_amount = goal.current_amount - expenses_total + income_total

        goal_summaries.append({
            'goal': goal,
            'expenses_total': expenses_total,
            'income_total': income_total,
            'total_amount': total_amount,
            'transactions': transactions
        })
    
    in_progress = total_goals - completed_goals

    # Use all goals (including hidden) to find last completed goal
    all_goals = Goal.query.filter_by(user_id=user_id).all()
    completed_goals_with_dates = [g for g in all_goals if g.date_completed is not None]
    last_completed_goal = max(completed_goals_with_dates, key=lambda g: g.date_completed, default=None)

    in_progress_goals = [
        {
            'goal': goal,
            'total_amount': total_amount,
            'progress': total_amount / goal.target_amount
        }
        for goal, total_amount in [(g['goal'], g['total_amount']) for g in goal_summaries]
        if total_amount < goal.target_amount and goal.target_amount > 0
    ]

    closest_to_completion = max(in_progress_goals, key=lambda x: x['progress'], default=None)

    return render_template('budgeting_and_goals/goals.html', form=form, summaries=goal_summaries, 
                           total_goals=total_goals, completed_goals=completed_goals, in_progress=in_progress, 
                           last_completed_goal=last_completed_goal, closest_to_completion=closest_to_completion, 
                           hidden_goals=hidden_goals, show_hidden=show_hidden)

@budgeting_and_goals_bp.route('/goals/edit/<int:goal_id>', methods=['GET', 'POST'])
@login_required 
def edit_goals(goal_id):
    goal = Goal.query.get_or_404(goal_id)

    # Ensure the user is the owner of the goal
    if goal.user_id != session['user']['id']:
        return redirect(url_for('budgeting_and_goals.view_goals', error='not_authorized_goal'))

    form = GoalForm(obj=goal)  # Pre-fill the form with the current goal values
    
    form.original_start_date.data = goal.start_date.strftime("%Y-%m-%d")

    if form.validate_on_submit():  # Save the changes when form is submitted

        goal.title = form.title.data
        goal.target_amount = form.target_amount.data
        goal.current_amount = form.current_amount.data
        goal.start_date = form.start_date.data
        goal.deadline = form.deadline.data
        goal.description = form.description.data

        db.session.commit()
    
        return redirect(url_for('budgeting_and_goals.view_goals', success='goal_edited'))
    else:
        print("Form errors:", form.errors)


    return render_template('budgeting_and_goals/goals_edit.html', form=form, goal_id=goal_id)

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

        return redirect(url_for('budgeting_and_goals.view_goals', success='goal_added'))
    else:
        print("Form errors:", form.errors)

    return render_template('budgeting_and_goals/goals_add.html', form=form)

@budgeting_and_goals_bp.route('/goals/delete/<int:goal_id>', methods=['POST'])
@login_required
def delete_goal(goal_id):
    goal = Goal.query.get_or_404(goal_id)

    if goal.user_id != session['user']['id']:
        return redirect(url_for('budgeting_and_goals.view_goals', error='not_authorized_goal'))

    db.session.delete(goal)
    db.session.commit()
    
    return redirect(url_for('budgeting_and_goals.view_goals', success='goal_deleted'))

@budgeting_and_goals_bp.route('/goal/<int:goal_id>/complete', methods=['POST'])
@login_required
def complete_goal(goal_id):
    user_id = session['user']['id']
    goal = Goal.query.filter_by(id=goal_id, user_id=user_id).first_or_404()

    if not goal.date_completed:
        goal.date_completed = datetime.now(timezone.utc)
        try:
            db.session.commit()
        except SQLAlchemyError:
            db.session.rollback()
            return redirect(url_for('budgeting_and_goals.view_goals', error='goal_update_failed'))
        
        return redirect(url_for('budgeting_and_goals.view_goals', success='goal_completed'))

    return redirect(url_for('budgeting_and_goals.view_goals', success='goal_already_completed'))

@budgeting_and_goals_bp.route('/goal/<int:goal_id>/toggle_hide', methods=['POST'])
@login_required
def toggle_hide_goal(goal_id):
    user_id = session['user']['id']
    goal = Goal.query.filter_by(id=goal_id, user_id=user_id).first()
    
    goal.is_hidden = not goal.is_hidden
    db.session.commit()

    action = "hidden" if goal.is_hidden else "visible"
    return redirect(url_for('budgeting_and_goals.view_goals', success=f'goal_{action}'))