# Documentation is like sex.
# When it's good, it's very good.
# When it's bad, it's better than nothing.
# When it lies to you, it may be a while before you realize something's wrong.

from sqlalchemy import UniqueConstraint

from app import db


class Transaction(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    date_validation = db.Column(db.DateTime)
    date_booking = db.Column(db.DateTime)
    amount_out = db.Column(db.Numeric(precision=2))
    amount_in = db.Column(db.Numeric(precision=2))
    balance = db.Column(db.Numeric(precision=2))
    transaction_entity = db.Column(db.String(256))
    comment = db.Column(db.String(256))
    purpose_code = db.Column(db.String(4))

    user_comment = db.relationship('UserComment', backref='transaction', lazy='dynamic')

    __table_args__ = (UniqueConstraint("date_validation", "date_booking", "amount_out", "amount_in",
                                       "balance", "transaction_entity", "comment", "purpose_code",
                                       name='_transaction_uc'),)


class Category(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(32), nullable=False)

    user_comment = db.relationship('UserComment', backref='category', lazy='dynamic')


class UserComment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    comment = db.Column(db.String(1024))

    category_id = db.Column(db.Integer, db.ForeignKey('category.id'))
    transaction_id = db.Column(db.Integer, db.ForeignKey('transaction.id'), nullable=False)
