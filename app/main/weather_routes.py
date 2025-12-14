from flask import render_template, redirect, url_for, flash, request
from datetime import datetime
from app.models import Travel, TravelItem, Item
from app import db
from . import main_bp
from app.services.openmeteo import get_daily_weather

@main_bp.route("/travel/<int:travel_id>/weather", methods=["POST"])
def travel_weather(travel_id):
    travel = Travel.query.get_or_404(travel_id)
    
    # 既存データチェック（16日以内かつ保存済みか）
    if not travel.weather_data or travel.weather_last_update is None \
        or (datetime.now() - travel.weather_last_update).days >= 1:

        # OpenMeteoから天気データを取得して保存
        travel.weather_data = get_daily_weather(travel.latitude, travel.longitude, travel.departure_date, travel.return_date)
        travel.weather_last_update = datetime.now()
        db.session.commit()
    
    return redirect(url_for("main.pickup_weather_items", travel_id=travel_id))

@main_bp.route("/travel/<int:travel_id>/weather-items")
def pickup_weather_items(travel_id):
    travel = Travel.query.get_or_404(travel_id)
    
    # 天気タイプ(sunny,rain...)抽出
    weather_types = { day["weather"]["type"] for day in travel.weather_data }

    candidates = Item.query.filter(Item.for_weather.in_(weather_types)).all()

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
    # -----------------------------------------------------   

    return render_template(
        "items_list.html", 
        travel=travel, 
        candidates=candidates,
        items_category=items_category,
        category_order=category_order    
    )
