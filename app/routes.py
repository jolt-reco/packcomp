from flask import Blueprint, render_template

bp = Blueprint("main", __name__)

@bp.route("/")
def index():
    return render_template("index.html")

@bp.route("/form")
def travel_form():
    return render_template("form.html")

@bp.route("/list")
def item_list():
    return render_template("list.html")