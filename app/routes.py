from sqlalchemy.exc import IntegrityError
from flask import render_template, request, flash, redirect, url_for
from . import app, db
from .models import Transaction
from config import DB_IMPORT_FILE_PATH
from .common.netstik.netstikreport import NetstikReport
from .common.db_helpers import get_all_transactions, get_transaction_header


# Documentation is like sex.
# When it's good, it's very good.
# When it's bad, it's better than nothing.
# When it lies to you, it may be a while before you realize something's wrong.

ALLOWED_EXTENSIONS = {"txt", }


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


@app.route('/', methods=["GET", "POST"])
def show():
    if request.method == "POST":
        if "report_file" not in request.files:
            flash("No file part")
            return redirect(url_for("show"))

        file = request.files["report_file"]
        if file.filename == '':
            flash("Datoteka ni izbrana", category="error")
            return redirect(url_for("show"))

        if file and allowed_file(file.filename):
            file.save(DB_IMPORT_FILE_PATH)
            import_success, reason = import_all(DB_IMPORT_FILE_PATH)
            if import_success:
                flash("Uspešno uvoženo")
            else:
                flash(f"Uvoz ni uspel: {str(reason)}", category="error")
            return redirect(url_for("show"))
        else:
            flash("Dovoljene vrste datotek so [csv]", category="error")
            return redirect(url_for("show"))

    elif request.method == "GET":
        return render_template("netstik_report/netstik_report.html",
                               transactions=get_all_transactions(),
                               transaction_header=get_transaction_header())
    return "Hello World!"
