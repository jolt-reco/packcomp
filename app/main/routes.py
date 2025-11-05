from flask import render_template, request, redirect, url_for, flash
from flask_login import current_user, login_required
from app import db
from app.models import Travel, Item
from datetime import datetime
from app.main import main_bp
from sqlalchemy import and_, or_

@main_bp.route("/")
def top():
    return render_template("top.html")

@main_bp.route("/travels")
@login_required
def travels_list():
    travels = Travel.query.filter_by(user_id=current_user.id).all()
    return render_template("travels_list.html", travels=travels)

@main_bp.route("/delete_travel/<int:travel_id>", methods=["GET", "POST"])
@login_required
def delete_travel(travel_id):
    travel = Travel.query.get_or_404(travel_id)

    if travel.user_id != current_user.id:
        flash("他のユーザーの旅行は削除できません", "danger")
        return redirect(url_for("main.travels_list"))
    
    try:
        db.session.delete(travel)
        db.session.commit()
        flash("旅行を削除しました", "success")
    except Exception as e:
        db.session.rollback()
        flash(f"削除に失敗しました{e}", "danger")
    return redirect(url_for("main.travels_list"))

@main_bp.route("/form", methods=["GET", "POST"])
@login_required
def new_travel():
    if request.method == "POST":
        try:
            title = request.form["title"]
            destination = request.form["destination"]
            departure_date = datetime.strptime(request.form["departure_date"], "%Y-%m-%d").date()
            return_date = datetime.strptime(request.form["return_date"], "%Y-%m-%d").date()
            male_count = int(request.form.get("male_count") or 0)
            female_count = int(request.form.get("female_count") or 0)
            child_count = int(request.form.get("child_count") or 0)
            purpose = ""
            transport = request.form.get("transport", "")

            new_travel = Travel(
                user_id=current_user.id,
                title=title,
                destination=destination,
                departure_date=departure_date,
                return_date=return_date,
                male_count=male_count,
                female_count=female_count,
                child_count=child_count,
                purpose=purpose,
                transport=transport
            )

            db.session.add(new_travel)
            db.session.commit()
            flash("旅行を登録しました！", "success")
            return redirect(url_for("main.items", travel_id=new_travel.id))
        
        except Exception as e:
            db.session.rollback()
            flash(f"登録に失敗しました: {e}", "error")             

    return render_template("new_travel.html")

@main_bp.route("/list/<int:travel_id>", methods=["GET", "POST"])
def items(travel_id):
    travel = Travel.query.get_or_404(travel_id)

    gender = travel.gender

    month = travel.depature_date.month
    if month in [12, 1, 2, 3]:
        season = "winter"
    elif month in [4, 5, 6]:
        season = "spring"
    elif month in [7, 8, 9]:
        season = "summer"
    else:
        season = "autumn"

    transport = travel.transport
    weather = travel.weather
    days = travel.days

    items = Item.query.filter(
        and_(
            Item.for_gender.in_([gender, "all"]),
            Item.for_season.in_([season, "all"]),
            Item.for_transport.in_([transport, "all"]),
            Item.for_weather.in_([weather, "all"]),
            or_(Item.min_days.is_(None), Item.min_days <= days),
            or_(Item.max_days.is_(None), Item.max_days >= days)
        )
    ).all()


    return render_template(
        "items_list.html",
        travel=travel,
        items=items
    )

@main_bp.route("/travel/<int:travel_id>/select_purpose", methods=["GET", "POST"])
@login_required
def select_purpose(travel_id):
    travel = Travel.query.get_or_404(travel_id)

    if request.method == "POST":
        travel.purpose = request.form["purpose"]
        db.session.commit()
        return redirect(url_for("main.items_list", travel_id=travel.id))

    return render_template("select_purpose.html", travel=travel)
