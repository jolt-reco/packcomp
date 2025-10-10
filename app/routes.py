from flask import Blueprint, render_template

bp = Blueprint("main", __name__)

@bp.route("/")
def index():
    return render_template("index.html")

@bp.route("/form")
def travel_form():
    return render_template("new_travel.html")