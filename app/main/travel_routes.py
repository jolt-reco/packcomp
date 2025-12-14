from flask import render_template, request, redirect, url_for, flash
from flask_login import login_required, current_user
from datetime import datetime
from app import db
from app.models import Travel, TravelPurpose, Purpose
from itertools import groupby
from . import main_bp
from .utils.item_generation import apply_diff_generation


@main_bp.route("/travels")
@login_required
def travels_list():
    travels = Travel.query.filter_by(user_id=current_user.id).order_by(Travel.departure_date).all()
    return render_template("travels_list.html", travels=travels)

@main_bp.route("/delete_travel/<int:travel_id>", methods=["POST"])
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
    except Exception:
        db.session.rollback()
        flash(f"削除に失敗しました", "danger")
    return redirect(url_for("main.travels_list"))

@main_bp.route("/form", methods=["GET", "POST"])
@login_required
def new_travel():
    if request.method == "POST":
        try:
            title = request.form["title"]
            destination = request.form["destination"]

            # Google Maps から緯度経度を取得
            lat = request.form.get("lat")
            lon = request.form.get("lon")

            if not lat or not lon:
                flash("必ずGoogleマップの候補から目的地を選択してください", "error")
                return redirect(url_for("main.new_travel"))

            departure_date = datetime.strptime(request.form["departure_date"], "%Y-%m-%d").date()
            return_date = datetime.strptime(request.form["return_date"], "%Y-%m-%d").date()
            male_count = int(request.form.get("male_count") or 0)
            female_count = int(request.form.get("female_count") or 0)
            child_count = int(request.form.get("child_count") or 0)
            transport = request.form.getlist("transport", "")

            new_travel = Travel(
                user_id=current_user.id,
                title=title,
                destination=destination,
                latitude=lat,
                longitude=lon,
                departure_date=departure_date,
                return_date=return_date,
                male_count=male_count,
                female_count=female_count,
                child_count=child_count,
                transport=transport
            )

            db.session.add(new_travel)
            db.session.commit()
            flash("旅行を登録しました！", "success")
            return redirect(url_for("main.select_purpose", travel_id=new_travel.id))
        
        except Exception:
            db.session.rollback()
            flash(f"登録に失敗しました", "error")             

    return render_template("new_travel.html")

@main_bp.route("/travel/<int:travel_id>/edit", methods=["GET", "POST"])
def edit_travel(travel_id):
    travel = Travel.query.get_or_404(travel_id)

    # 他のユーザーの編集を防ぐ
    if travel.user_id != current_user.id:
        flash("この旅行情報を編集する権限がありません。", "error")
        return redirect(url_for("main.travels_list"))

    if request.method == "POST":
        try:
            # フォームから更新
            travel.title = request.form["title"]
            travel.destination = request.form["destination"]
            travel.latitude = request.form.get("lat")
            travel.longitude = request.form.get("lon")
            travel.departure_date = datetime.strptime(request.form["departure_date"], "%Y-%m-%d").date()
            travel.return_date = datetime.strptime(request.form["return_date"], "%Y-%m-%d").date()
            travel.male_count = int(request.form.get("male_count") or 0)
            travel.female_count = int(request.form.get("female_count") or 0)
            travel.child_count = int(request.form.get("child_count") or 0)
            travel.transport = request.form.getlist("transport", "")

            # 天気情報をリセット
            travel.weather_data = None
            travel.weather_last_update = None

            db.session.commit()
            flash("旅行情報を更新しました。", "success")
            return redirect(url_for("main.select_purpose", travel_id=travel_id))
        
        except Exception:
            db.session.rollback()
            flash(f"更新に失敗しました", "error") 

    # GETの場合はフォームに既存データを渡す
    return render_template("edit_travel.html", travel=travel)

@main_bp.route("/travel/<int:travel_id>/select_purpose", methods=["GET", "POST"])
@login_required
def select_purpose(travel_id):
    travel = Travel.query.get_or_404(travel_id)

    # 登録済みのpurposeを取得(編集時ハイライト用)
    pre_selected_purposes = [tp.purpose_id for tp in travel.travel_purposes]

    if request.method == "POST":
        selected = request.form.get("purposes")
        new_ids = set(int(x) for x in selected.split(',') if x)
        current_ids = set(pre_selected_purposes)
        
        for pid in current_ids - new_ids:
            tp = TravelPurpose.query.filter_by(travel_id=travel_id, purpose_id=pid).first()
            if tp:
                db.session.delete(tp)

        for pid in new_ids - current_ids:
            tp = TravelPurpose(travel_id=travel_id, purpose_id=pid)
            db.session.add(tp)       

        db.session.commit()

        # 持ち物リストの差分生成適用
        apply_diff_generation(travel_id)

        return redirect(url_for("main.items", travel_id=travel_id))

    purposes = Purpose.query.order_by(Purpose.category).all()
    grouped_purposes = { 
        category: list(purposes_in_cat) 
        for category, purposes_in_cat in groupby(purposes, key=lambda x: x.category)
        }
    return render_template(
        "select_purpose.html", 
        grouped_purposes=grouped_purposes, 
        travel=travel,
        pre_selected_purposes=pre_selected_purposes
    )

