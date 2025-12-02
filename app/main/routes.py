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
from app.services.nominatim import geocode
from app.services.openmeteo import get_daily_weather

UPLOAD_FOLDER = "app/static/uploads"
ALLOWED_EXTENSIONS = {"png", "jpg", "jpeg", "gif"}


@main_bp.route("/")
def top():
    return render_template("top.html")

@main_bp.route("/terms")
def terms():
    return render_template("terms.html")

@main_bp.route("/privacy")
def privacy():
    return render_template("privacy.html")

@main_bp.route("/contact")
def contact():
    return render_template("contact.html")

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
            transport = request.form.getlist("transport", "")

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

@main_bp.route("/travel/<int:travel_id>/edit", methods=["GET", "POST"])
def edit_travel(travel_id):
    travel = Travel.query.get_or_404(travel_id)

    # 他のユーザーの編集を防ぐ
    if travel.user_id != current_user.id:
        flash("この旅行情報を編集する権限がありません。", "error")
        return redirect(url_for("main.travels_list"))

    if request.method == "POST":
        # フォームから更新
        travel.title = request.form["title"]
        travel.departure_date = datetime.strptime(request.form["departure_date"], "%Y-%m-%d").date()
        travel.return_date = datetime.strptime(request.form["return_date"], "%Y-%m-%d").date()
        travel.male_count = int(request.form.get("male_count") or 0)
        travel.female_count = int(request.form.get("female_count") or 0)
        travel.child_count = int(request.form.get("child_count") or 0)
        travel.transport = request.form.getlist("transport", "")

        db.session.commit()
        flash("旅行情報を更新しました。", "success")
        return redirect(url_for("main.travels_list"))

    # GETの場合はフォームに既存データを渡す
    return render_template("edit_travel.html", travel=travel)

@main_bp.route("/travel/<int:travel_id>/weather", methods=["POST"])
def travel_weather(travel_id):
    travel = Travel.query.get_or_404(travel_id)

    destination = travel.destination
    departure_date = travel.departure_date
    return_date = travel.return_date

    lat, lon = geocode(destination)
    if lat is None:
        return "場所が見つかりませんでした"

    daily_weather = get_daily_weather(lat, lon, departure_date, return_date)
    
    # ---------items_category生成のための重複コード-----------
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
            "id": disp_ti.id,
            "name": name,
            "category": category,
            "quantity": disp_ti.quantity
        })

        display_items = sorted(display_items, key=lambda x: (x["category"], x["name"]))


    items_category = {}

    for di in display_items:
        cat = di["category"]
        items_category.setdefault(cat, []).append(di)

    # -----------------------------------------------------   

    return render_template("items_list.html", travel=travel, items_category=items_category, daily_weather=daily_weather)

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

    existing_items = TravelItem.query.filter_by(travel_id=travel.id).all()
    if not existing_items:
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
            "id": disp_ti.id,
            "name": name,
            "category": category,
            "quantity": disp_ti.quantity
        })

        display_items = sorted(display_items, key=lambda x: (x["category"], x["name"]))


    items_category = {}

    for di in display_items:
        cat = di["category"]
        items_category.setdefault(cat, []).append(di)

    return render_template(
        "items_list.html",
        travel=travel,
        items_category=items_category
    )

@main_bp.route("/update_quantities/<int:travel_id>", methods=["POST"])
@login_required
def update_quantities(travel_id):
    for key, value in request.form.items():
        if not key.startswith("qty_"):
            continue
        try:
            item_id = int(key.replace("qty_", ""))
        except (IndexError, ValueError):
            continue 
        
        qty = int(value)

        ti = TravelItem.query.get(item_id)
        if ti and ti.travel_id == travel_id:
            ti.quantity = qty

    db.session.commit()
    return redirect(url_for('main.items', travel_id=travel_id))

@main_bp.route("/list/<int:travel_id>/delete/<int:item_id>", methods=["POST"])
@login_required
def delete_item(travel_id, item_id):
    ti = TravelItem.query.get_or_404(item_id)
    db.session.delete(ti)
    db.session.commit()

    return "", 200

@main_bp.route("/list/<int:travel_id>/reset", methods=["POST"])
@login_required
def reset_items(travel_id):
    # TravelItem 全削除
    TravelItem.query.filter_by(travel_id=travel_id).delete()
    db.session.commit()

    # items へ戻る → 初期生成が走る
    return redirect(url_for("main.items", travel_id=travel_id))


@main_bp.route("/travel/<int:travel_id>/select_purpose", methods=["GET", "POST"])
@login_required
def select_purpose(travel_id):
    travel = Travel.query.get_or_404(travel_id)

    pre_selected_purposes = [tp.purpose_id for tp in travel.travel_purposes]

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
    return render_template(
        "select_purpose.html", 
        grouped_purposes=grouped_purposes, 
        travel=travel,
        pre_selected_purposes=pre_selected_purposes
    )

@main_bp.route("/custom_item/<int:travel_id>", methods=["GET", "POST"])
@login_required
def custom_items_list(travel_id):
    travel = Travel.query.get_or_404(travel_id)
    custom_items = CustomItem.query.filter_by(
        user_id=current_user.id
    ).all()

    return render_template(
        "custom_items_list.html",
        custom_items=custom_items,
        travel=travel
    )

@main_bp.route("/custom_item/new/<int:travel_id>", methods=["GET", "POST"])
@login_required
def new_custom_item(travel_id):
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
        return redirect(url_for("main.custom_items_list", travel_id=travel_id))
    
    categories = db.session.query(Item.category).distinct().all()
    categories = [c[0] for c in categories]
    return render_template("custom_items_form.html", categories=categories, travel_id=travel_id)

@main_bp.route("/travel/<int:travel_id>/add_custom_item", methods=["POST"])
@login_required
def add_custom_to_travel(travel_id):
    custom_item_id = request.form.get("custom_item_id")
    if not custom_item_id:
        flash("アイテムIDがありません")
        return redirect(url_for("main.custom_items_list"))

    exists = TravelItem.query.filter_by(
        travel_id=travel_id,
        custom_item_id=custom_item_id
    ).first()
    if exists:
        flash("すでにリストに追加されています")
        return redirect(url_for("main.items", travel_id=travel_id))

    cus_ti = TravelItem(
        travel_id=travel_id,
        item_id=None,
        custom_item_id=custom_item_id,
        my_set_item_id=None,
        quantity=1,
        note=None,
        check_flag=False
    )
    db.session.add(cus_ti)
    db.session.commit()
    flash("アイテムを持ち物リストに追加しました")
    return redirect(url_for("main.items", travel_id=travel_id))

@main_bp.route("/custom_item/<int:travel_id>/delete/<int:item_id>", methods=["POST"])
@login_required
def delete_custom_item(travel_id, item_id):
    ci = CustomItem.query.get_or_404(item_id)
    db.session.delete(ci)
    db.session.commit()

    return "", 200

@main_bp.route("/myset/create", methods=["POST"])
@login_required
def new_myset():
    data = request.get_json()

    myset_name = data.get("name")
    item_ids = data.get("item_ids", [])
    travel_id = data.get("travel_id")

    if not myset_name or not item_ids:
        return {"error": "invalid data"}, 400

    # ① マイセット本体登録
    new_myset = MySet(
        name=myset_name,
        user_id=current_user.id
    )
    db.session.add(new_myset)
    db.session.commit()  # ここで new_myset.id が確定

    # ② MySetItems の登録
    for tid in item_ids:
        ti = TravelItem.query.get(tid)
        if ti is None:
            continue

        new_item = MySetItem(
            my_set_id=new_myset.id,
            item_id=ti.item_id,
            custom_item_id=ti.custom_item_id,
        )
        db.session.add(new_item)

    db.session.commit()

    return "", 200   

@main_bp.route("/mysets/<int:travel_id>")
@login_required
def mysets_list(travel_id):
    travel = Travel.query.get_or_404(travel_id)
    mysets = MySet.query.filter_by(user_id=current_user.id).all()

    return render_template(
        "mysets_list.html",
        travel=travel,
        mysets=mysets
    )

@main_bp.route("/myset/<int:my_set_id>/items")
@login_required
def get_myset_items(my_set_id):
    items = (
        db.session.query(MySetItem, Item, CustomItem)
        .outerjoin(Item, MySetItem.item_id == Item.id)
        .outerjoin(CustomItem, MySetItem.custom_item_id == CustomItem.id)
        .filter(MySetItem.my_set_id == my_set_id)
        .all()
    )

    result = []
    for ms_item, item, citem in items:
        result.append({
            "name": item.name if item else citem.name,
            "category": item.category if item else citem.category
        })

    return {"items": result}, 200

@main_bp.route("/myset/<int:my_set_id>/add_myset/<int:travel_id>", methods=["POST"])
@login_required
def add_myset_to_travel(my_set_id, travel_id):

    items = MySetItem.query.filter_by(my_set_id=my_set_id).all()

    existing_item_ids = {
        (ti.item_id, ti.custom_item_id)
        for ti in TravelItem.query.filter_by(travel_id=travel_id).all()
    }

    # TravelItem にコピーして追加
    for ms_item in items:
        key = (ms_item.item_id, ms_item.custom_item_id)
        if key in existing_item_ids:
            continue  # 同じアイテムならスキップ

        new_ti = TravelItem(
            travel_id=travel_id,
            item_id=ms_item.item_id,
            custom_item_id=ms_item.custom_item_id,
            quantity=1  # 数量は1で初期化（あとでユーザーが調整）
        )
        db.session.add(new_ti)

    db.session.commit()

    flash("マイセットを持ち物リストに追加しました")
    return redirect(url_for("main.items", travel_id=travel_id))

@main_bp.route("/myset/<int:my_set_id>/delete", methods=["POST"])
@login_required
def delete_myset(my_set_id):
    myset = MySet.query.get_or_404(my_set_id)
    if myset.user_id != current_user.id:
        return "", 403

    # 関連する MySetItem もまとめて削除
    MySetItem.query.filter_by(my_set_id=myset.id).delete()
    db.session.delete(myset)
    db.session.commit()
    return "", 200

@main_bp.route("/myset/<int:travel_id>/edit/<int:my_set_id>")
@login_required
def edit_myset(my_set_id, travel_id):
    myset = MySet.query.filter_by(id=my_set_id, user_id=current_user.id).first_or_404()
    ms_items = MySetItem.query.filter_by(my_set_id=my_set_id).all()

    all_items = Item.query.all()
    all_custom_items = CustomItem.query.all()

    display_items = []
    for disp_mi in ms_items:
        if disp_mi.item:
            name = disp_mi.item.name
            category = disp_mi.item.category
        elif disp_mi.custom_item:
            name = disp_mi.custom_item.name
            category = disp_mi.custom_item.category
        else:
            name = "不明"
            category = "その他"

        display_items.append({
            "id": disp_mi.id,
            "name": name,
            "category": category,
        })

    display_items = sorted(display_items, key=lambda x: (x["category"], x["name"]))
    
    items_category = {}

    for di in display_items:
        cat = di["category"]
        items_category.setdefault(cat, []).append(di)

    return render_template(
        "edit_myset.html",
        myset=myset,
        ms_items=ms_items,
        all_items=all_items,
        all_custom_items=all_custom_items,
        items_category=items_category,
        travel_id=travel_id
    )

@main_bp.route("/myset/<int:my_set_id>/item/<int:ms_item_id>/delete", methods=["POST"])
@login_required
def delete_myset_item(my_set_id, ms_item_id):
    ms_item = MySetItem.query.filter_by(id=ms_item_id, my_set_id=my_set_id).first_or_404()
    db.session.delete(ms_item)
    db.session.commit()
    flash("削除しました")
    return redirect(url_for("main.edit_myset", my_set_id=my_set_id))

@main_bp.route("/myset/<int:travel_id>/add_items/<int:my_set_id>")
@login_required
def add_items_to_myset(travel_id, my_set_id):

    myset = MySet.query.filter_by(id=my_set_id, user_id=current_user.id).first_or_404()

    display_items = []
    display_custom_items = []

    # Item → 辞書へ
    for item in Item.query.all():
        display_items.append({
            "id": item.id,
            "name": item.name,
            "category": item.category
        })

    display_items = sorted(display_items, key=lambda x: (x["category"], x["name"]))

    # CustomItem → 辞書へ
    for ci in CustomItem.query.filter_by(user_id=current_user.id).all():
        display_custom_items.append({
            "id": ci.id,
            "name": ci.name,
            "category": ci.category
        })

    display_custom_items = sorted(display_custom_items, key=lambda x: (x["category"], x["name"]))

    items_category = {}
    custom_items_category = {}
    for di in display_items:
        cat = di["category"]
        items_category.setdefault(cat, []).append(di)

    for dci in display_custom_items:
        cat = dci["category"]
        custom_items_category.setdefault(cat, []).append(dci)

    return render_template(
        "add_items_to_myset.html",
        myset=myset,
        items_category=items_category,
        custom_items_category=custom_items_category,
        travel_id=travel_id
    )

@main_bp.route("/myset/<int:travel_id>/add_items/<int:my_set_id>", methods=["POST"])
@login_required
def add_items_to_myset_post(travel_id, my_set_id):
    data = request.get_json()
    item_ids = data.get("item_ids", [])
    custom_ids = data.get("custom_ids", [])

    # 標準アイテム追加
    for item_id in item_ids:
        db.session.add(MySetItem(my_set_id=my_set_id, item_id=item_id))

    # カスタムアイテム追加
    for ci_id in custom_ids:
        db.session.add(MySetItem(my_set_id=my_set_id, custom_item_id=ci_id))

    db.session.commit()

    # 追加後、編集画面へ飛ばす
    return redirect(url_for(
        "main.edit_myset",
        my_set_id=my_set_id,
        travel_id=travel_id
    ))
