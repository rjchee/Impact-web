from sqlalchemy import and_

from app import db


preferences_table = db.Table('preferences_helper',
    db.Column('user_id', db.Integer, db.ForeignKey('user.id'), primary_key=True),
    db.Column('category_id', db.Integer, db.ForeignKey('category.id'), primary_key=True)
)


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    account = db.relationship('Account', uselist=False, back_populates='owner')
    lat = db.Column(db.Float(10))
    lng = db.Column(db.Float(10))
    preferences = db.relationship('Category', secondary=preferences_table)
    score = db.Column(db.Float(5))
    profile_picture = db.Column(db.String(80))

    def __init__(self, n):
        self.username = n
        self.account = Account()
        self.score = 5.0


class Account(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    owner_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    owner = db.relationship('User', back_populates='account')
    entries = db.relationship('Entry')

    def add_entry(self, val, categories):
        categories = set(categories)
        entry = None
        for e in self.entries:
            if categories == set(c.name for c in e.categories):
                entry = e
                break
        if entry:
            entry.value += val
        else:
            entry = Entry(val, categories)
            self.entries.append(entry)


account_table = db.Table('account_helper',
    db.Column('entry_id', db.Integer, db.ForeignKey('entry.id'), primary_key=True),
    db.Column('category_id', db.Integer, db.ForeignKey('category.id'), primary_key=True)
)


class Entry(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    value = db.Column(db.Numeric(10, 2), nullable=False)
    account_id = db.Column(db.Integer, db.ForeignKey('account.id'))
    categories = db.relationship('Category', secondary=account_table)

    def __init__(self, val, categories):
        self.value = val
        self.categories = Category.query.filter(Category.name.in_(categories)).all()


class Category(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique=True, nullable=False)

    def __init__(self, n):
        self.name = n

    def __str__(self):
        return self.name

    def __repr__(self):
        return 'Category({})'.format(self.name)


donation_table = db.Table('donation_helper',
    db.Column('donation_id', db.Integer, db.ForeignKey('donation.id'), primary_key=True),
    db.Column('category_id', db.Integer, db.ForeignKey('category.id'), primary_key=True)
)

class Donation(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    value = db.Column(db.Numeric(10, 2), nullable=False)
    categories = db.relationship('Category', secondary=donation_table)
    sender_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    sender = db.relationship('User', backref='sent_donations', foreign_keys=[sender_id])
    receiver_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    receiver = db.relationship('User', backref='received_donations', foreign_keys=[receiver_id])

    def __init__(self, sender, receiver, value, categories):
        self.sender = sender
        self.receiver = receiver
        self.value = value
        self.categories = Category.query.filter(Category.name.in_(categories)).all()
