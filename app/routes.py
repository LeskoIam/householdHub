# Documentation is like sex.
# When it's good, it's very good.
# When it's bad, it's better than nothing.
# When it lies to you, it may be a while before you realize something's wrong.

from flask import render_template, request, flash, redirect, url_for

from config import DB_IMPORT_FILE_PATH
from . import app
from .common.common import allowed_file
from .common.hue.hue import Hue, BRIDGE_IP, CRED_FILE_PATH
from .common.db_helpers import import_all, get_all_transactions, get_transaction_header


@app.route("/")
@app.route("/index")
def index():
    return render_template("index.html")


# ######################
# Finances
# ######################
@app.route("/finances")
def finances():
    return render_template("finances/finances.html")


@app.route("/finances/netstik-report", methods=["GET", "POST"])
def netstik_report():
    if request.method == "POST":
        if "report_file" not in request.files:
            flash("No file part")
            return redirect(url_for("netstik_report"))

        file = request.files["report_file"]
        if file.filename == '':
            flash("Datoteka ni izbrana", category="error")
            return redirect(url_for("netstik_report"))

        if file and allowed_file(file.filename):
            file.save(DB_IMPORT_FILE_PATH)
            import_success, reason = import_all(DB_IMPORT_FILE_PATH)
            if import_success:
                flash("Uspešno uvoženo")
            else:
                flash(f"Uvoz ni uspel: {str(reason)}", category="error")
            return redirect(url_for("netstik_report"))
        else:
            flash("Dovoljene vrste datotek so [csv]", category="error")
            return redirect(url_for("netstik_report"))

    elif request.method == "GET":
        return render_template("finances/netstik/netstik_report.html",
                               transactions=get_all_transactions(),
                               transaction_header=get_transaction_header())
    return "Hello World!"


# ######################
# Hue
# ######################


@app.route("/hue", methods=["GET", "POST"])
def hue():
    if request.method == "GET":
        return render_template("hue/hue.html")
    elif request.method == "POST":
        with open(CRED_FILE_PATH, "r") as cred_file:
            username = cred_file.read()
        import time
        h = Hue(BRIDGE_IP, username)
        h.find_all_lights()
        lights = h.lights
        lights[9]("state", on=True)
        time.sleep(1)
        lights[9]("state", on=False)
        time.sleep(1)

    return "zmaj"
