from flask import render_template, request, redirect, url_for, flash
from flask_login import login_required
from app import db
from app.models import Travel, TravelItem, Item
from . import main_bp
from .utils.item_generation import apply_diff_generation
from app import csrf

@main_bp.route("/travel/<int:travel_id>/auto-items", methods=["POST"])
def auto_items_post(travel_id):
    travel = Travel.query.get_or_404(travel_id)
    
    # 天気アイテムモーダル(_candidates_item.html)より選択済みアイテムを取得
    selected_ids = request.form.getlist("item_ids")
    selected_items = Item.query.filter(Item.id.in_(selected_ids)).all()
    
    # 既存のTravelItemを確認(重複追加防止)
    existing_items = TravelItem.query.filter_by(travel_id=travel.id).all()
    existing_item_ids = {ti.item_id for ti in existing_items}

    for item in selected_items:
        if item.id in existing_item_ids:
            continue

        if item.for_gender == "male":
            quantity = travel.male_count
        elif item.for_gender == "female":
            quantity = travel.female_count
        elif item.for_gender == "child":
            quantity = travel.child_count
        else:
            quantity = travel.male_count + travel.female_count + travel.child_count

        add_ti = TravelItem(
            my_set_item_id=None,
            item_id=item.id,
            custom_item_id=None,
            travel_id=travel_id,
            quantity=quantity,
            note=None,
            check_flag=False,
            auto_added=True
        )
        db.session.add(add_ti)
    db.session.commit()
    flash("アイテムを追加しました", "success")

    return redirect(url_for("main.items", travel_id=travel_id))


@main_bp.route("/list/<int:travel_id>", methods=["GET"])
def items(travel_id):
    travel = Travel.query.get_or_404(travel_id)

    travel_items = TravelItem.query.filter_by(travel_id=travel_id).all()
    
    # 表示用リスト作成
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

    # 天気アイテム再取得用リスト
    candidates = []
    if travel.weather_data:
        weather_types = { day["weather"]["type"] for day in travel.weather_data }
        candidates = Item.query.filter(Item.for_weather.in_(weather_types)).all()

    return render_template(
        "items_list.html",
        travel=travel,
        items_category=items_category,
        category_order=category_order,
        candidates=candidates
    )

@main_bp.route("/update_quantities/<int:travel_id>", methods=["POST"])
@login_required
def update_quantities(travel_id):
    # form内のvalues(qty_)を取得して更新
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

@csrf.exempt
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

    # 差分生成適用(この場合は全追加になる)
    apply_diff_generation(travel_id)
   
    return redirect(url_for("main.items", travel_id=travel_id))

