from flask import render_template, request, redirect, url_for, flash
from flask_login import current_user, login_required
from app import db
from app.models import (
    Travel,
    Item, 
    Purpose, 
    TravelPurpose, 
    PurposeItem, 
    CustomItem, 
    TravelItem,
    MySet,
    MySetItem
)
from datetime import datetime
from app.main import main_bp
from sqlalchemy import and_, or_
from itertools import groupby
import os
from werkzeug.utils import secure_filename

UPLOAD_FOLDER = "app/static/uploads"
ALLOWED_EXTENSIONS = {"png", "jpg", "jpeg", "gif"}


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
                transport=transport
            )

            db.session.add(new_travel)
            db.session.commit()
            flash("旅行を登録しました！", "success")
            return redirect(url_for("main.select_purpose", travel_id=new_travel.id))
        
        except Exception as e:
            db.session.rollback()
            flash(f"登録に失敗しました: {e}", "error")             

    return render_template("new_travel.html")

@main_bp.route("/list/<int:travel_id>", methods=["GET", "POST"])
def items(travel_id):
    travel = Travel.query.get_or_404(travel_id)

    month = travel.departure_date.month
    if month in [12, 1, 2, 3]:
        season = "winter"
    elif month in [4, 5, 6]:
        season = "spring"
    elif month in [7, 8, 9]:
        season = "summer"
    else:
        season = "autumn"

    transport = travel.transport
    weather = "all"
    days = (travel.return_date - travel.departure_date).days + 1

    purpose_ids = [
        tp.purpose_id for tp in TravelPurpose.query.filter_by(travel_id=travel_id).all()
        ]

    item_ids = [
        pi.item_id for pi in PurposeItem.query.filter(PurposeItem.purpose_id.in_(purpose_ids)).all()
        ]

    my_set_ids =[
        mi.id for mi in MySet.query.filter(MySet.user_id == current_user.id).all()
    ]

    purpose_items = Item.query.filter(
        Item.id.in_(item_ids),
        and_(
            Item.for_season.in_([season, "all"]),
            Item.for_transport.in_([transport, "all"]),
            Item.for_weather.in_([weather, "all"]),
            or_(Item.min_days.is_(None), Item.min_days <= days),
            or_(Item.max_days.is_(None), Item.max_days >= days)
        )
    ).all()

    general_items = Item.query.filter(
        ~Item.id.in_(PurposeItem.query.with_entities(PurposeItem.item_id).subquery()),
        Item.for_season.in_([season, "all"]),
        Item.for_transport.in_([transport, "all"]),
        Item.for_weather.in_([weather, "all"]),
        or_(Item.min_days.is_(None), Item.min_days <= days),
        or_(Item.max_days.is_(None), Item.max_days >= days)
    ).all()

    custom_items = CustomItem.query.filter_by(
        user_id=current_user.id
    ).all()

    my_set_items = MySetItem.query.filter(
        MySetItem.my_set_id.in_(my_set_ids)
    ).all()

    ini_items = purpose_items + general_items
    for item in ini_items:
        exists = TravelItem.query.filter_by(
            travel_id=travel_id,
            item_id=item.id
        ).first()
        if exists:
            continue

        if item.for_gender == "male":
            quantity = travel.male_count
        elif item.for_gender == "female":
            quantity = travel.female_count
        elif item.for_gender == "child":
            quantity = travel.child_count
        else:
            quantity = travel.male_count + travel.female_count + travel.child_count

        ini_ti = TravelItem(
            my_set_item_id=None,
            item_id=item.id,
            custom_item_id=None,
            travel_id=travel_id,
            quantity=quantity,
            note=None,
            check_flag=False
        )
        db.session.add(ini_ti)
    db.session.commit()
    
    for cus_item in custom_items:
        exists = TravelItem.query.filter_by(
            travel_id=travel_id,
            custom_item_id=cus_item.id
        ).first()
        if exists:
            continue

        ti = TravelItem(
            my_set_item_id=None,
            item_id=None,
            custom_item_id=cus_item.id,
            travel_id=travel_id,
            quantity=1,
            note=None,
            check_flag=False
        )
        db.session.add(ti)
    db.session.commit()
    
    for mys_item in my_set_items:
        exists = TravelItem.query.filter_by(
            travel_id=travel_id,
            my_set_item_id=mys_item.id
        ).first()
        if exists:
            continue
        
        same_item = TravelItem.query.filter_by(
            travel_id=travel_id,
            item_id=mys_item.item_id
        ).first()
        if same_item:
            continue

        mi = TravelItem(
            my_set_item_id=mys_item.id,
            item_id=None,
            custom_item_id=None,
            travel_id=travel_id,
            quantity=1,
            note=None,
            check_flag=False
        )
        db.session.add(mi)
    db.session.commit()

    travel_items = TravelItem.query.filter_by(travel_id=travel_id).all()

    display_items = []
    for disp_ti in travel_items:
        if disp_ti.item:
            name = disp_ti.item.name
            category = disp_ti.item.category
        elif disp_ti.custom_item:
            name = disp_ti.custom_item.name
            category = disp_ti.custom_item.category
        else:
            disp_mi=disp_ti.my_set_item
            if disp_mi and disp_mi.item:
                name = disp_mi.item.name
                category = disp_mi.item.category
            elif disp_mi and disp_mi.custom_item:
                name = disp_mi.custom_item.name
                category = disp_mi.custom_item.category
            else:
                name = "不明"
                category = "その他"

        display_items.append({
            "name": name,
            "category": category,
            "quantity": disp_ti.quantity
        })

    items_category = {}

    for di in display_items:
        cat = di["category"]
        items_category.setdefault(cat, []).append(di)

    return render_template(
        "items_list.html",
        travel=travel,
        items_category=items_category
    )

@main_bp.route("/travel/<int:travel_id>/select_purpose", methods=["GET", "POST"])
@login_required
def select_purpose(travel_id):
    travel = Travel.query.get_or_404(travel_id)

    if request.method == "POST":
        selected = request.form.get("purposes", "")
        purpose_ids = [int(x) for x in selected.split(',') if x]
        
        TravelPurpose.query.filter_by(travel_id=travel_id).delete()

        for pid in purpose_ids:
            tp = TravelPurpose(travel_id=travel_id, purpose_id=pid)
            db.session.add(tp)
        db.session.commit()
        return redirect(url_for("main.items", travel_id=travel_id))

    purposes = Purpose.query.order_by(Purpose.category).all()
    grouped_purposes = { 
        category: list(purposes_in_cat) 
        for category, purposes_in_cat in groupby(purposes, key=lambda x: x.category)
        }
    return render_template("select_purpose.html", grouped_purposes=grouped_purposes, travel=travel)
@main_bp.route("/custom_item", methods=["GET", "POST"])
@login_required
def custom_items_list():
    custom_items = CustomItem.query.filter_by(
        user_id=current_user.id
    ).all()

    return render_template(
        "custom_item_list.html",
        custom_items=custom_items
    )

@main_bp.route("/custom_item/new", methods=["GET", "POST"])
@login_required
def new_custom_item():
    if request.method == "POST":
        name = request.form["name"]
        category = request.form["category"]
        note = request.form.get("note")
        image_file = request.files.get("image")
        image_path = None
        if image_file and image_file.filename:
            filename = secure_filename(image_file.filename)
            path = os.path.join(UPLOAD_FOLDER, filename)
            image_file.save(path)
            image_path = f"/static/uploads/{filename}"

        new_item = CustomItem(
            user_id=current_user.id,
            name=name,
            category=category,
            note=note,
            image_path=image_path
        )
        db.session.add(new_item)
        db.session.commit()
        flash("アイテムを追加しました!")
        return redirect(url_for("main.custom_items_list"))
    
    categories = db.session.query(Item.category).distinct().all()
    categories = [c[0] for c in categories]
    return render_template("custom_items_form.html", categories=categories)