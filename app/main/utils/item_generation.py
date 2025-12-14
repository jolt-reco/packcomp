from sqlalchemy import and_, or_
from app import db

def apply_diff_generation(travel_id):

    from app.models import Travel, TravelItem, Item, TravelPurpose, PurposeItem

    travel = Travel.query.get(travel_id)
    
    # 旅行条件の基礎情報を算出
    month = travel.departure_date.month
    if month in [12, 1, 2, 3]:
        season = "winter"
    elif month in [7, 8, 9]:
        season = "summer"
    else:
        season = "mid"

    transport = travel.transport or []
    days = (travel.return_date - travel.departure_date).days + 1

    # TravelPurpose → PurposeItem 取得
    purpose_ids = [
        tp.purpose_id for tp in TravelPurpose.query.filter_by(travel_id=travel_id).all()
    ]

    item_ids = [
        pi.item_id for pi in PurposeItem.query.filter(
            PurposeItem.purpose_id.in_(purpose_ids)
        ).all()
    ]

    # 性別フィルタ
    allowed_genders = ["all"]
    if travel.male_count > 0:
        allowed_genders.append("male")
    if travel.female_count > 0:
        allowed_genders.append("female")

    # 目的別アイテム
    purpose_items = Item.query.filter(
        Item.id.in_(item_ids),
        and_(
            Item.is_general == False,
            Item.for_gender.in_(allowed_genders),
            Item.for_season.in_([season, "all"]),
            Item.for_weather == "all",
            or_(Item.min_days.is_(None), Item.min_days <= days),
            or_(Item.max_days.is_(None), Item.max_days >= days)
        )
    ).all()

    # 共通アイテム
    general_items = Item.query.filter(
        ~Item.id.in_(PurposeItem.query.with_entities(PurposeItem.item_id).subquery()),
        Item.is_general == True,
        Item.for_gender.in_(allowed_genders),
        Item.for_season.in_([season, "all"]),
        Item.for_weather == "all",
        or_(Item.min_days.is_(None), Item.min_days <= days),
        or_(Item.max_days.is_(None), Item.max_days >= days)
    ).all()

    # transport によるフィルタ（手動）
    filtered_purpose_items = [
        item for item in purpose_items
        if ("all" in item.for_transport or any(t in item.for_transport for t in transport))
    ]

    filtered_general_items = [
        item for item in general_items
        if ("all" in item.for_transport or any(t in item.for_transport for t in transport))
    ]

    # 差分生成処理

    # 既存
    existing_items = TravelItem.query.filter_by(travel_id=travel.id).all()
    existing_item_ids = {ti.item_id for ti in existing_items if ti.item_id}

    # 新規にあるべき item_id
    new_item_ids = {item.id for item in filtered_purpose_items + filtered_general_items}

    # 1) 削除アイテム（custom_item は除外）
    for ti in existing_items:
        if ti.custom_item_id:
            continue

        # "auto_added" を考慮しないなら：
        if ti.item_id not in new_item_ids:
            db.session.delete(ti)

    # 2) 新規追加アイテム
    for item in filtered_purpose_items + filtered_general_items:
        if item.id in existing_item_ids:
            continue

        # 数量の初期値ロジック
        if item.fixed_quantity is not None:
            quantity = item.fixed_quantity
        else:
            if item.for_gender == "male":
                quantity = travel.male_count
            elif item.for_gender == "female":
                quantity = travel.female_count
            elif item.for_gender == "child":
                quantity = travel.child_count
            else:
                quantity = travel.male_count + travel.female_count + travel.child_count

        # TravelItem 追加
        ini_ti = TravelItem(
            my_set_item_id=None,
            item_id=item.id,
            custom_item_id=None,
            travel_id=travel.id,
            quantity=quantity,
            note=None,
            check_flag=False,
        )
        db.session.add(ini_ti)

    db.session.commit()

