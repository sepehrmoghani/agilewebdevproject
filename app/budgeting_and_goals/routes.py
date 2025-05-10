from datetime import date
from flask import Blueprint, render_template, request, redirect, url_for, flash
from .forms import BudgetForm, GoalForm
from .models import Budget, Goal
from app import db

budgeting_and_goals_bp = Blueprint(
    'budgeting_and_goals_bp', __name__, template_folder='templates', static_folder='static'
)

# Budgeting
@budgeting_and_goals_bp.route('/budget', methods=['GET'])
#@login_required
def view_budget():
    form = BudgetForm()
    user_id = 1  # Placeholder for the logged-in user's ID
    # Query the budgets created by the currently logged-in user
    user_budgets = Budget.query.filter_by(user_id=user_id).all()
    
    return render_template('budgeting_and_goals/budget.html', form=form, budgets=user_budgets)

@budgeting_and_goals_bp.route('/budget/edit/<int:id>', methods=['GET', 'POST'])
#@login_required
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
        
        db.session.commit()  # Save to the database
        flash("Budget updated successfully!", "success")
        return redirect(url_for('budgeting_and_goals_bp.view_budget'))  # Redirect after save

    return render_template('budgeting_and_goals/budget_edit.html', form=form, budget_id=id)

@budgeting_and_goals_bp.route('/budget/add', methods=['GET', 'POST'])
#@login_required  # Make sure the user is logged in
def add_budget():
    form = BudgetForm()  # Create a new form for adding a budget

    if form.validate_on_submit():  # Validate form data when submitted
        # Create a new Budget instance with form data
        user_id = 1  # Placeholder for the logged-in user's ID
        new_budget = Budget(
            category=form.category.data,
            limit=form.limit.data,
            period=form.period.data,
            user_id=user_id  # Set the user_id to the current user's id
        )
        
        db.session.add(new_budget)  
        db.session.commit()  

        flash('Budget added successfully!', 'success') 
        return redirect(url_for('budgeting_and_goals_bp.view_budget'))  # Redirect to view the budget list

    return render_template('budgeting_and_goals/budget_add.html', form=form)

@budgeting_and_goals_bp.route('/budget/delete/<int:id>', methods=['POST'])
#@login_required
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



# Goals
@budgeting_and_goals_bp.route('/goals', methods=['GET'])
#@login_required
def view_goals():
    form = GoalForm()
    user_id = 1  # Placeholder for the logged-in user's ID
    user_goals = Goal.query.filter_by(user_id=user_id).all()

    return render_template('budgeting_and_goals/goals.html', form=form, goals=user_goals)

@budgeting_and_goals_bp.route('/goals/edit/<int:id>', methods=['GET', 'POST'])
#@login_required
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

        db.session.commit()
        flash("Goal updated successfully!", "success")
        return redirect(url_for('budgeting_and_goals_bp.view_goals'))

    return render_template('budgeting_and_goals/goals_edit.html', form=form, goal_id=id)

@budgeting_and_goals_bp.route('/goals/add', methods=['GET', 'POST'])
#@login_required  # Ensure the user is logged in
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
            user_id=user_id
        )

        db.session.add(new_goal)
        db.session.commit()

        flash('Goal added successfully!', 'success')
        return redirect(url_for('budgeting_and_goals_bp.view_goals'))  # Redirect to view the goals list

    return render_template('budgeting_and_goals/goals_add.html', form=form)

@budgeting_and_goals_bp.route('/goals/delete/<int:id>', methods=['POST'])
#@login_required
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
