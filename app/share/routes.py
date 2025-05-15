from flask import render_template, request, jsonify, abort, redirect, url_for, session, flash
from . import share_bp
from .models import ShareSettings
from .forms import ShareForm
from app.transactions.models import Transaction
from app.authentication.models import User
from app import db
import uuid
from datetime import datetime, timedelta
from sqlalchemy import func

@share_bp.route('/share', methods=['GET', 'POST'])
def share_settings():
    if 'user' not in session:
        return redirect(url_for('authentication.login'))

    user_id = session['user']['id']
    share_settings = ShareSettings.query.filter_by(user_id=user_id).first()

    categories = db.session.query(Transaction.category)\
        .filter(Transaction.user_id == user_id)\
        .distinct()\
        .all()
    categories = [cat[0] for cat in categories if cat[0]]

    if not share_settings:
        share_settings = ShareSettings(
            user_id=user_id,
            share_url=str(uuid.uuid4())[:8],
            is_public=False
        )
        db.session.add(share_settings)
        db.session.commit()

    selected_categories = share_settings.selected_categories.split(',') if share_settings.selected_categories else []

    if request.method == 'POST':
        selected = request.form.getlist('categories')
        share_settings.selected_categories = ','.join(selected)
        db.session.commit()
        flash('Share settings updated!', 'success')
        return redirect(url_for('share.share_settings'))

    form = ShareForm()
    return render_template('share/share.html', 
                         form=form,
                         categories=categories,
                         share_settings=share_settings,
                         selected_categories=selected_categories)

@share_bp.route('/toggle_share', methods=['POST'])
def toggle_share():
    if 'user' not in session:
        return jsonify({'success': False}), 401

    data = request.get_json()
    user_id = session['user']['id']
    share_settings = ShareSettings.query.filter_by(user_id=user_id).first()

    if share_settings:
        share_settings.is_public = data.get('is_public', False)
        db.session.commit()
        return jsonify({'success': True, 'is_public': share_settings.is_public})

    return jsonify({'success': False}), 404

@share_bp.route('/shared/<share_url>')
def view_shared(share_url):
    share_settings = ShareSettings.query.filter_by(share_url=share_url).first()

    if not share_settings:
        abort(404)

    user = User.query.get(share_settings.user_id)

    if not share_settings.is_public:
        return render_template('share/shared_view.html', 
                             is_private=True,
                             username=f"{user.first_name} {user.last_name}")

    selected_categories = share_settings.selected_categories.split(',') if share_settings.selected_categories else []
    improvements = calculate_improvements(share_settings.user_id, selected_categories)

    return render_template('share/shared_view.html',
                         is_private=False,
                         username=f"{user.first_name} {user.last_name}",
                         categories=selected_categories,
                         improvements=improvements)


def calculate_improvements(user_id, categories):
    improvements = {}
    today = datetime.now().date()

    # Get current week's Monday
    this_week_start = today - timedelta(days=today.weekday())
    this_week_end = this_week_start + timedelta(days=7)
    last_week_start = this_week_start - timedelta(days=7)
    last_week_end = this_week_start - timedelta(days=1)

    print("today:", today)
    print("this_week_start:", this_week_start)
    print("this_week_end:", this_week_end)
    print("last_week_start:", last_week_start)
    print("last_week_end:", last_week_end)

    print(Transaction.date)

    for category in categories:
        # Current week = this_week_start to today (or this_week_start + 7)
        current_week = db.session.query(func.sum(Transaction.amount)).filter(
            Transaction.user_id == user_id,
            Transaction.category == category,
            func.date(Transaction.date) >= this_week_start,
            func.date(Transaction.date) < this_week_end,
            Transaction.transaction_type == 'expense'
        ).scalar() or 0


        print("current_week:", current_week)

        # Previous week = last_week_start to last_week_end
        previous_week = db.session.query(func.sum(Transaction.amount)).filter(
            Transaction.user_id == user_id,
            Transaction.category == category,
            func.date(Transaction.date) >= last_week_start,
            func.date(Transaction.date) < last_week_end,
            Transaction.transaction_type == 'expense'
        ).scalar() or 0

        print("previous_week:", previous_week)

        if previous_week == 0 and current_week == 0:
            improvements[category] = 0
        elif previous_week == 0:
            improvements[category] = -100
        else:
            improvement = ((previous_week - current_week) / previous_week) * 100
            improvements[category] = round(improvement)

    return improvements

