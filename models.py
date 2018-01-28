from sqlalchemy import and_

from app import db

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    account = db.relationship('Account', uselist=False, back_populates='owner')

    def __init__(self, n):
        self.username = n
        self.account = Account()


class Account(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    owner_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    owner = db.relationship('User', back_populates='account')
    entries = db.relationship('Entry')

    def add_entry(self, val, categories):
        categories = set(categories)
        with db.session.begin():
            entry = None
            for e in entries:
                if categories == set(c.name for c in e.categories):
                    entry = e
                    break
            if entry:
                entry.value += val
            else:
                entry = Entry(val, categories)
                self.entries.append(entry)
            db.session.commit()


account_table = db.Table('account_helper',
    db.Column('entry_id', db.Integer, db.ForeignKey('entry.id'), primary_key=True),
    db.Column('category_id', db.Integer, db.ForeignKey('category.id'), primary_key=True)
)


class Entry(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    value = db.Column(db.Numeric(10, 2), nullable=False)
    account_id = db.Column(db.Integer, db.ForeignKey('account.id'))
    categories = db.relationship('Category', secondary=account_table, backref='entries')

    def __init__(self, val, categories):
        self.value = val
        self.categories = Category.query.filter(Category.name.in_(categories)).all()


class Category(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique=True, nullable=False)

    def __init__(self, n):
        self.name = n
