# Documentation is like sex.
# When it's good, it's very good.
# When it's bad, it's better than nothing.
# When it lies to you, it may be a while before you realize something's wrong.

from sqlalchemy.exc import IntegrityError

from app import db
from app.models import Transaction
if __name__ == '__main__':
    from netstik.netstikreport import NetstikReport
else:
    from .netstik.netstikreport import NetstikReport


def get_all_transactions():
    return Transaction.query.all()


def get_transaction_header():
    return Transaction.__table__.columns.keys()


def import_all(report_file: str):
    report = NetstikReport(report_file=report_file)
    for trans in report.transactions:
        tr = Transaction(date_validation=trans.date_1,
                         date_booking=trans.date_2,
                         amount_out=trans.amount_out,
                         amount_in=trans.amount_in,
                         balance=trans.balance,
                         transaction_entity=trans.person,
                         comment=trans.comment,
                         purpose_code=trans.purpose_code)
        db.session.add(tr)
    try:
        db.session.commit()
    except IntegrityError as exc:
        return False, str(exc)
    return True, None


if __name__ == '__main__':
    get_all_transactions()

    print(db.engine.url.database)
    print(db.engine.url.drivername)