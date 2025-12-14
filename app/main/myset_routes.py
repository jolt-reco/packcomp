from flask import render_template, request, redirect, url_for, flash
from flask_login import login_required, current_user
from app import db
from app.models import Travel, MySet, MySetItem, TravelItem, Item, CustomItem
from . import main_bp
from app import csrf

@csrf.exempt
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
    db.session.commit() 

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
            continue 

        new_ti = TravelItem(
            travel_id=travel_id,
            item_id=ms_item.item_id,
            custom_item_id=ms_item.custom_item_id,
            quantity=1
        )
        db.session.add(new_ti)

    db.session.commit()

    flash("マイセットを持ち物リストに追加しました", "success")
    return redirect(url_for("main.items", travel_id=travel_id))

@csrf.exempt
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

@csrf.exempt
@main_bp.route("/myset/<int:my_set_id>/item/<int:ms_item_id>/delete", methods=["POST"])
@login_required
def delete_myset_item(my_set_id, ms_item_id):
    ms_item = MySetItem.query.filter_by(id=ms_item_id, my_set_id=my_set_id).first_or_404()
    db.session.delete(ms_item)
    db.session.commit()
    return "", 200

@csrf.exempt
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

    # CustomItem → 辞書へ
    for ci in CustomItem.query.filter_by(user_id=current_user.id).all():
        display_custom_items.append({
            "id": ci.id,
            "name": ci.name,
            "category": ci.category
        })

    items_category = {}
    custom_items_category = {}
    for di in display_items:
        cat = di["category"]
        items_category.setdefault(cat, []).append(di)

    for dci in display_custom_items:
        cat = dci["category"]
        custom_items_category.setdefault(cat, []).append(dci)

    category_order = [
        "衣類", 
        "生活用品", 
        "電子機器", 
        "書類・貴重品", 
        "衛生・健康", 
        "美容・スキンケア", 
        "天候用品", 
        "季節用品", 
        "交通関連", 
        "収納用品", 
        "ペット同伴用品", 
        "アウトドア用品", 
        "その他"
    ]

    return render_template(
        "add_items_to_myset.html",
        myset=myset,
        items_category=items_category,
        custom_items_category=custom_items_category,
        category_order=category_order,
        travel_id=travel_id
    )

@main_bp.route("/myset/<int:travel_id>/add_items/<int:my_set_id>", methods=["POST"])
@login_required
def add_items_to_myset_post(travel_id, my_set_id):
    data = request.get_json()
    item_ids = data.get("item_ids", [])
    custom_ids = data.get("custom_ids", [])

    for item_id in item_ids:
        db.session.add(MySetItem(my_set_id=my_set_id, item_id=item_id))

    for ci_id in custom_ids:
        db.session.add(MySetItem(my_set_id=my_set_id, custom_item_id=ci_id))

    db.session.commit()

    return redirect(url_for(
        "main.edit_myset",
        my_set_id=my_set_id,
        travel_id=travel_id
    ))
