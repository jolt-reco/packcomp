from flask import render_template, request, redirect, url_for, flash
from flask_login import login_required, current_user
from app import db
from app.models import Travel, CustomItem, TravelItem, Item
from . import main_bp

@main_bp.route("/custom_item/<int:travel_id>", methods=["GET"])
@login_required
def custom_items_list(travel_id):
    travel = Travel.query.get_or_404(travel_id)
    custom_items = CustomItem.query.filter_by(
        user_id=current_user.id
    ).all()

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

    custom_items_category = {}
    for ci in custom_items:
        custom_items_category.setdefault(ci.category, []).append(ci)

    return render_template(
        "custom_items_list.html",
        custom_items_category=custom_items_category,
        category_order=category_order,
        travel=travel
    )

@main_bp.route("/custom_item/new/<int:travel_id>", methods=["GET", "POST"])
@login_required
def new_custom_item(travel_id):
    if request.method == "POST":
        name = request.form["name"]
        category = request.form["category"]
        note = request.form.get("note")
        image_path = None

        new_item = CustomItem(
            user_id=current_user.id,
            name=name,
            category=category,
            note=note,
            image_path=image_path
        )
        db.session.add(new_item)
        db.session.commit()
        flash("アイテムを追加しました!", "success")
        return redirect(url_for("main.custom_items_list", travel_id=travel_id))
    
    # Itemのcategory一覧を取得(formのセレクトボックス用)
    categories = db.session.query(Item.category).distinct().all()
    categories = [c[0] for c in categories]
    return render_template("custom_items_form.html", categories=categories, travel_id=travel_id)

@main_bp.route("/travel/<int:travel_id>/add_custom_item", methods=["POST"])
@login_required
def add_custom_to_travel(travel_id):
    custom_item_ids = request.form.getlist("custom_item_ids")
    if not custom_item_ids:
        flash("アイテムがありません", "error")
        return redirect(url_for("main.custom_items_list", travel_id=travel_id))

    for custom_item_id in custom_item_ids:
        exists = TravelItem.query.filter_by(
            travel_id=travel_id,
            custom_item_id=custom_item_id
        ).first()

        # 既にTravelItemにて存在する場合はスキップ
        if exists:
            continue
        
        # TravelItemに新規追加
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

    flash("アイテムを持ち物リストに追加しました", "success")
    return redirect(url_for("main.items", travel_id=travel_id))

@main_bp.route("/custom_item/<int:travel_id>/delete/<int:item_id>", methods=["POST"])
@login_required
def delete_custom_item(travel_id, item_id):
    ci = CustomItem.query.get_or_404(item_id)
    try:
        # 該当custom_item_idを持つTravelItemを削除
        travel_items = TravelItem.query.filter_by(custom_item_id=item_id).all()
        for ti in travel_items:
            db.session.delete(ti)
        db.session.delete(ci)
        db.session.commit()

    except Exception as e:
        db.session.rollback()


    return "", 200

