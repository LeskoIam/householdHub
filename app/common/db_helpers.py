# Documentation is like sex.
# When it's good, it's very good.
# When it's bad, it's better than nothing.
# When it lies to you, it may be a while before you realize something's wrong.
import hashlib

from sqlalchemy import desc
from sqlalchemy.exc import IntegrityError

from app import db
from app.models import Transaction
if __name__ == '__main__':
    from netstik.netstikreport import NetstikReport
else:
    from .netstik.netstikreport import NetstikReport


def get_all_transactions():
    return Transaction.query.order_by(desc(Transaction.date_booking)).all()


def get_transaction_header():
    return Transaction.__table__.columns.keys()


def import_all(report_file: str):
    report = NetstikReport(report_file=report_file)
    reason = ""
    success = True
    for trans in report.transactions:
        tr = Transaction(date_validation=trans.date_1,
                         date_booking=trans.date_2,
                         amount_out=trans.amount_out,
                         amount_in=trans.amount_in,
                         balance=trans.balance,
                         transaction_entity=trans.person,
                         comment=trans.comment,
                         purpose_code=trans.purpose_code,
                         # TODO: T1. Workaround
                         thash=hash_them(trans.date_1,
                                         trans.date_2,
                                         trans.amount_out,
                                         trans.amount_in,
                                         trans.balance,
                                         trans.person,
                                         trans.comment,
                                         trans.purpose_code))
        db.session.add(tr)
        try:
            db.session.commit()
        except IntegrityError as exc:
            reason += f" {str(exc)} |"
            success = False
            db.session.rollback()
    return success, reason


def hash_them(*args):
    args = "".join([str(x) for x in args]).encode()
    return hashlib.sha256(args).hexdigest()


if __name__ == '__main__':
    def jea():
        data = Transaction.query.order_by(desc(Transaction.date_booking)).all()
        for d in data:
            # d = "".join([str(x) for x in [d.date_validation,
            #                               d.date_booking,
            #                               d.amount_out,
            #                               d.amount_in,
            #                               d.balance,
            #                               d.transaction_entity,
            #                               d.comment,
            #                               d.purpose_code]]).encode()
            # hexd = hashlib.sha224(d).hexdigest()
            print(hash_them(*[d.date_validation,
                              d.date_booking,
                              d.amount_out,
                              d.amount_in,
                              d.balance,
                              d.transaction_entity,
                              d.comment,
                              d.purpose_code]))
    jea()

    get_all_transactions()

    print(db.engine.url.database)
    print(db.engine.url.drivername)
