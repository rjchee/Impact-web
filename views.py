from collections import defaultdict
from decimal import Decimal

from flask import jsonify, render_template, request

from app import app, db
from models import *

# Frontend functions
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/dashboard')
def dashboard():
    return render_template('dashboard.html')

# API Functions

def error(message):
    return jsonify({'error': message, 'success': False}), 400

@app.route('/api/user/new', methods=['POST'])
def create_user():
    username = request.form.get('username')
    if not username:
        return error('no username specified')
    lat = request.form.get('lat')
    lng = request.form.get('lng')
    prefs = request.form.getlist('categories')
    preflist = Category.query.filter(Category.name.in_(prefs)).all()
    try:
        user = User(username)
        if lat:
            user.lat = lat
        if lng:
            user.lng = lng
        user.preferences = preflist
        db.session.add(user)
        db.session.commit()
        return jsonify({'success': True})
    except:
        return error('the username already exists')

@app.route('/api/user/edit', methods=['POST'])
def edit_user():
    username = request.form.get('username')
    if not username:
        return error('no username specified')
    user = User.query.filter_by(username=username).first()
    if user is None:
        return error('no user "{}" found'.format(username))
    lat = request.form.get('lat')
    lng = request.form.get('lng')
    if lat:
        user.lat = lat
    if lng:
        user.lng = lng
    prefs = request.form.getlist('categories')
    if prefs:
        user.preferences = Category.query.filter(Category.name.in_(prefs)).all()
    db.session.add(user)
    db.session.commit()
    return jsonify({'success': True})

@app.route('/api/user/donate', methods=['POST'])
def donate_money():
    sender = request.form.get('sender')
    receiver = request.form.get('receiver')
    value = request.form.get('value')
    categories = request.form.getlist('categories')
    if not sender:
        return error('no sender specified')
    if not receiver:
        return error('no receiver specified')
    if not value:
        return error('no amount of money specified')
    if not categories:
        return error('no categories specified')
    try:
        value = Decimal(value)
    except:
        return error('`value` should be a decimal')
    if value <= 0:
        return error('`value` should be positive')
    rcver = User.query.filter_by(username=receiver).first()
    if rcver is None:
        return error('user {} is not found'.format(receiver))
    snder = User.query.filter_by(username=sender).first()
    if snder is None:
        return error('user {} is not found'.format(sender))
    rcver.account.add_entry(value, categories)
    donation = Donation(snder, rcver, value, categories)
    db.session.add(donation)
    rcver.received_donations.append(donation)
    snder.sent_donations.append(donation)
    db.session.commit()
    return jsonify({'success': True})


def consolidate_donations(donations):
    aggregate = defaultdict(float)
    for donation in donations:
        aggregate[tuple(sorted(c.name for c in donation.categories))] += float(donation.value)
    result = []
    for categories, value in aggregate.items():
        result.append({
            'categories': list(categories),
            'value': value
        })
    return result

@app.route('/api/user/<username>', methods=['GET'])
def get_account(username):
    user = User.query.filter_by(username=username).first()
    if user is None:
        return error('user {} was not found'.format(username))
    balance = []
    for e in user.account.entries:
        balance.append({
            'categories': sorted([c.name for c in e.categories]),
            'value': float(e.value)
        })
    sent_donations = consolidate_donations(user.sent_donations)
    received_donations = consolidate_donations(user.received_donations)
    result = {'success': True, 'balance': balance, 'sent_donations_breakdown': sent_donations, 'received_donations_breakdown': received_donations}
    return jsonify(result)

@app.route('/api/users/', methods=['GET'])
def get_users():
    users = User.query.all()
    results = []
    for u in users:
        sent_donations = consolidate_donations(u.sent_donations)
        received_donations = consolidate_donations(u.received_donations)
        obj = {'sent_donations_breakdown': sent_donations, 'received_donations_breakdown': received_donations}
        results.append(obj)
    return jsonify({'success': True, 'users': results})

# Admin functions

@app.route('/admin')
def admin_page():
    users = User.query.all()
    return render_template('admin.html', users=users)
