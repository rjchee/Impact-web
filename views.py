from decimal import Decimal

from flask import jsonify, render_template, request

from app import app, db
from models import User, Account, Entry, Category

def error(message):
    return jsonify({'error': message, 'success': False}), 400

@app.route('/api/user/new', methods=['POST'])
def create_user():
    username = request.form.get('username')
    if not username:
        return error('no username specified')
    try:
        db.session.add(User(username))
        db.session.commit()
        return jsonify({'success': True})
    except:
        return error('the username already exists')

@app.route('/api/user/add', methods=['POST'])
def add_money():
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
    rcver.account.add_entry(value, categories)
    db.session.commit()
    return jsonify({'success': True})


@app.route('/api/user/<username>', methods=['GET'])
def get_account(username):
    user = User.query.filter_by(username=username).first()
    if user is None:
        return error('user {} was not found'.format(username))
    entries = []
    for e in user.account.entries:
        entries.append({
            'categories': [c.name for c in e.categories],
            'value': float(e.value)
        })
    result = {'success': True, 'entries': entries}
    return jsonify(result)


@app.route('/admin')
def admin_page():
    users = User.query.all()
    return render_template('admin.html', users=users)
