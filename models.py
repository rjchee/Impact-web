from app import db

from sqlalchemy.orm import relationship

class Donor(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)

class Donee(db.Model):
    id = Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    account = relationship('Account', uselist=False, back_populates='owner')

class Account(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    owner_id = db.Column(db.Integer, db.ForeignKey('owner.id'))
    owner = relationship('Donee', back_populates='account')
    entries = relationship('Entry')

account_table = db.Table('account_helper',
    db.Column('entry_id', db.Integer, db.ForeignKey('entry.id'), primary_key=True),
    db.Column('category_id', db.Integer, db.ForeignKey('category.id'), primary_key=True)
)

class Entry(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    value = db.Column(db.Numeric(10, 2), nullable=False)
    account_id = db.Column(db.Integer, db.ForeignKey('account.id'))
    categories = db.relationship('Category', secondary=account_table, backref='entries')

class Category(Model):
    id = Column(Integer, primary_key=True)
    name = Column(String(80), unique=True, nullable=False)
