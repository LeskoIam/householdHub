from app import db
from app.models import Transaction

# Documentation is like sex.
# When it's good, it's very good.
# When it's bad, it's better than nothing.
# When it lies to you, it may be a while before you realize something's wrong.


def get_all_transactions():
    return Transaction.query.all()


def get_transaction_header():
    return Transaction.__table__.columns.keys()


if __name__ == '__main__':
    get_all_transactions()

    print(db.engine.url.database)
    print(db.engine.url.drivername)