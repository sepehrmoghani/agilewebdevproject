from datetime import date, datetime, timedelta, timezone
from flask import Blueprint, render_template, request, redirect, url_for, flash
from .forms import BudgetForm, GoalForm
from .models import User, Budget, Goal
from app.transactions.models import Transaction
from app import db

budgeting_and_goals_bp = Blueprint(
    'budgeting_and_goals_bp', __name__, template_folder='templates', static_folder='static'
)

#Budgeting Helper Functions
def get_transactions_for_budget(user_id, category, period):
    # Get today's date
    today = datetime.now(timezone.utc).date()

    # Calculate date range based on period
    if period == 'weekly':
        start_date = today - timedelta(days=7)
    elif period == 'monthly':
        start_date = today - timedelta(days=30)
    elif period == 'yearly':
        start_date = today - timedelta(days=365)
    else:
        # fallback to the earliest possible aware date
        start_date = datetime(1, 1, 1, tzinfo=timezone.utc).date()

    # Query matching transactions
    transactions = Transaction.query.filter_by(
        user_id=user_id, #TODO: Replace with actual user_id
        category=category
    ).filter(
        Transaction.date >= datetime.combine(start_date, datetime.min.time(), tzinfo=timezone.utc)
    ).all()

    return transactions

# Budgeting
@budgeting_and_goals_bp.route('/budget', methods=['GET'])
#@login_required TODO:
def view_budget():
    form = BudgetForm()
    user_id = 1  # TODO: Placeholder for the logged-in user's ID
    # Query the budgets created by the currently logged-in user
    user_budgets = Budget.query.filter_by(user_id=user_id).all()
    
    budget_summaries = []

    for budget in user_budgets:
        transactions = get_transactions_for_budget(user_id, budget.category, budget.period)
        expenses_total = sum(t.amount for t in transactions if t.transaction_type == 'expense')
        income_total = sum(t.amount for t in transactions if t.transaction_type == 'income')

        total_spent = expenses_total - income_total

        budget_summaries.append({
            'budget': budget,
            'transactions': transactions,
            'total_spent': total_spent
        })
        
    return render_template('budgeting_and_goals/budget.html', form=form, summaries=budget_summaries)

@budgeting_and_goals_bp.route('/budget/edit/<int:id>', methods=['GET', 'POST'])
#@login_required TODO:
def edit_budget(id):
    budget = Budget.query.get_or_404(id)
    
    # Ensure the user is the owner of the budget
    user_id = 1  # Placeholder for the logged-in user's ID
    if user_id != user_id:
        flash("You do not have permission to edit this budget.", "danger")
        return redirect(url_for('budgeting_and_goals_bp.view_budget'))

    form = BudgetForm(obj=budget)  # Pre-fill the form with the current budget values

    if form.validate_on_submit():  # Save the changes when form is submitted
        # Update the budget with the new values from the form
        budget.category = form.category.data
        budget.limit = form.limit.data
        budget.period = form.period.data
        budget.description = form.description.data
        
        db.session.commit()  # Save to the database
        flash("Budget updated successfully!", "success")
        return redirect(url_for('budgeting_and_goals_bp.view_budget'))  # Redirect after save

    return render_template('budgeting_and_goals/budget_edit.html', form=form, budget_id=id)

@budgeting_and_goals_bp.route('/budget/add', methods=['GET', 'POST'])
#@login_required TODO:
def add_budget():
    form = BudgetForm()  # Create a new form for adding a budget

    if form.validate_on_submit():  # Validate form data when submitted
        # Create a new Budget instance with form data
        user_id = 1  # Placeholder for the logged-in user's ID
        new_budget = Budget(
            category=form.category.data,
            limit=form.limit.data,
            period=form.period.data,
            description=form.description.data,
            user_id=user_id  # Set the user_id to the current user's id
        )
        
        db.session.add(new_budget)  
        db.session.commit()  

        flash('Budget added successfully!', 'success') 
        return redirect(url_for('budgeting_and_goals_bp.view_budget'))  # Redirect to view the budget list

    return render_template('budgeting_and_goals/budget_add.html', form=form)

@budgeting_and_goals_bp.route('/budget/delete/<int:id>', methods=['POST'])
#@login_required TODO:
def delete_budget(id):
    budget = Budget.query.get_or_404(id)

    # Only allow deletion if the budget belongs to the current user
    user_id = 1  # Placeholder for the logged-in user's ID
    if budget.user_id != user_id:
        flash("You are not authorized to delete this budget.", "danger")
        return redirect(url_for('budgeting_and_goals_bp.view_budget'))

    db.session.delete(budget)
    db.session.commit()
    flash("Budget deleted successfully.", "success")
    return redirect(url_for('budgeting_and_goals_bp.view_budget'))


#Goal Helper Functions
def get_transactions_for_goal(user_id, start_date, deadline):
    """
    Fetch transactions for a given user between start_date and deadline.
    Separately totals expenses and income.
    """
    # Query all transactions in date range
    transactions = Transaction.query.filter_by(
        user_id = user_id, #TODO: Replace with actual user_id 
    ).filter(
        Transaction.date >= datetime.combine(start_date, datetime.min.time(), tzinfo=timezone.utc),
        Transaction.date <= datetime.combine(deadline, datetime.max.time(), tzinfo=timezone.utc)
    ).all()

    return transactions

# Goals
@budgeting_and_goals_bp.route('/goals', methods=['GET'])
#@login_required TODO:
def view_goals():
    form = GoalForm()
    user_id = 1  # TODO: Placeholder for the logged-in user's ID
    user_goals = Goal.query.filter_by(user_id=user_id).all()

    goal_summaries = []
    total_goals = len(user_goals)
    completed_goals = 0
    shared_goals = 0
    
    for goal in user_goals:
        # Get transactions between goal start and deadline
        transactions = get_transactions_for_goal(user_id, goal.start_date, goal.deadline)
        expenses_total = sum(t.amount for t in transactions if t.transaction_type == 'expense')
        income_total = sum(t.amount for t in transactions if t.transaction_type == 'income')
        
        total_amount = goal.current_amount - expenses_total + income_total

        if total_amount >= goal.target_amount:
            completed_goals += 1
        
        if goal.privacy:
            shared_goals += 1
        
        goal_summaries.append({
            'goal': goal,
            'expenses_total': expenses_total,
            'income_total': income_total,
            'total_amount': total_amount,
            'transactions': transactions
        })
    
    in_progress = total_goals - completed_goals
    
    return render_template('budgeting_and_goals/goals.html', form=form, summaries=goal_summaries, 
                           total_goals=total_goals, completed_goals=completed_goals, in_progress=in_progress, shared_goals=shared_goals)

@budgeting_and_goals_bp.route('/goals/edit/<int:id>', methods=['GET', 'POST'])
#@login_required TODO:
def edit_goals(id):
    goal = Goal.query.get_or_404(id)
    
    # Ensure the user is the owner of the goal
    user_id = 1  # Placeholder for the logged-in user's ID
    if user_id != user_id:
        flash("You do not have permission to edit this goal.", "danger")
        return redirect(url_for('budgeting_and_goals_bp.view_goals'))

    form = GoalForm(obj=goal)  # Pre-fill the form with the current goal values

    if form.validate_on_submit():  # Save the changes when form is submitted
        
        goal.title = form.title.data
        goal.target_amount = form.target_amount.data
        goal.current_amount = form.current_amount.data
        goal.start_date = form.start_date.data
        goal.deadline = form.deadline.data
        goal.description = form.description.data
        goal.privacy = form.privacy.data == 'public'  # Convert to boolean

        db.session.commit()
        flash("Goal updated successfully!", "success")
        return redirect(url_for('budgeting_and_goals_bp.view_goals'))
    elif request.method == 'GET':
        form.privacy.data = 'public' if goal.privacy else 'private'


    return render_template('budgeting_and_goals/goals_edit.html', form=form, goal_id=id)

@budgeting_and_goals_bp.route('/goals/add', methods=['GET', 'POST'])
#@login_required TODO:
def add_goal():
    form = GoalForm()  # Create a new form for adding a goal

    if form.validate_on_submit():  # Validate form data when submitted
        
        user_id = 1
        new_goal = Goal(
            title=form.title.data,
            target_amount=form.target_amount.data,
            current_amount=form.current_amount.data,
            start_date=form.start_date.data,
            deadline=form.deadline.data,
            description=form.description.data,
            privacy=form.privacy.data == 'public',  # Convert to boolean
            user_id=user_id
        )

        db.session.add(new_goal)
        db.session.commit()

        flash('Goal added successfully!', 'success')
        return redirect(url_for('budgeting_and_goals_bp.view_goals'))  # Redirect to view the goals list

    return render_template('budgeting_and_goals/goals_add.html', form=form)

@budgeting_and_goals_bp.route('/goals/delete/<int:id>', methods=['POST'])
#@login_required TODO:
def delete_goal(id):
    goal = Goal.query.get_or_404(id)

    user_id = 1  # Placeholder for the logged-in user's ID
    if goal.user_id != user_id:
        flash("You are not authorized to delete this goal.", "danger")
        return redirect(url_for('budgeting_and_goals_bp.view_goals'))

    db.session.delete(goal)
    db.session.commit()
    flash("Goal deleted successfully.", "success")
    return redirect(url_for('budgeting_and_goals_bp.view_goals'))

@budgeting_and_goals_bp.route('/goals/shared', methods=['GET'])
def shared_goals():
    public_goals = Goal.query.filter_by(privacy=True).all()

    goal_summaries = []

    for goal in public_goals:
        user_id = goal.user_id
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

    return render_template('budgeting_and_goals/shared_goals.html', summaries=goal_summaries)
