# Documentation is like sex.
# When it's good, it's very good.
# When it's bad, it's better than nothing.
# When it lies to you, it may be a while before you realize something's wrong.

from config import ALLOWED_EXTENSIONS
from app.models import Transaction
from app import db
from .netstik.netstikreport import NetstikReport
from sqlalchemy.exc import IntegrityError


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


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
