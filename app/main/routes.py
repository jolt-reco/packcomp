from flask import render_template, request, redirect, url_for, flash
from flask_login import current_user, login_required
from app import db
from app.models import Travel
from datetime import datetime
from app.main import main_bp

@main_bp.route("/")
def top():
    return render_template("top.html")

@main_bp.route("/travels")
@login_required
def travels_list():
    travels = Travel.query.filter_by(user_id=current_user.id).all()
    return render_template("travels_list.html", travels=travels)

@main_bp.route("/form")
@login_required
def new_travel():
    if request.method == "POST":
        try:
            title = request.form["title"]
            destination = request.form["destination"]
            departure_date = datetime.strptime(request.form["departure_date"], "%Y-%m-%d").date()
            return_date = datetime.strptime(request.form["return_date"], "%Y-%m-%d").date()
            male_count = int(request.form.get("male_count", 0))
            female_count = int(request.form.get("female_count", 0))
            child_count = int(request.form.get("child_count", 0))
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
            return redirect(url_for("main.travel_list"))
        
        except Exception as e:
            db.session.rollback()
            flash(f"登録に失敗しました: {e}", "error")             

    return render_template("new_travel.html")

@main_bp.route("/list", methods=["POST"])
def items():
    # travel情報の受信(テスト用のみの記述:削除予定)
        travel_title = request.form.get("title")
        destination = request.form.get("destination")
        male_count = request.form.get("male_count")
        female_count = request.form.get("female_count")
        child_count = request.form.get("child_count")

    # 仮アイテムの受信(削除予定)
        mock_items = [
            {"name": "歯ブラシ", "quantity": 1},
            {"name": "パスポート", "quantity": 1},
            {"name": "オムツ", "quantity": child_count},
        ]

        return render_template(
            "items_list.html",
            title=travel_title,
            destination=destination,
            items=mock_items
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
