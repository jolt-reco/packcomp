from app import create_app, db
from app.models import Purpose, Item, PurposeItem

def seed_purpose():
    data = [
        {"name": "観光", "category": "定番"},
        {"name": "温泉", "category": "定番"},
        {"name": "食べ歩き", "category": "定番"},
        {"name": "帰省", "category": "定番"},
        {"name": "写真旅", "category": "定番"},
        {"name": "ドライブ", "category": "定番"},
        {"name": "ペット同伴", "category": "定番"},

        {"name": "海水浴", "category": "レジャー"},
        {"name": "登山", "category": "レジャー"},
        {"name": "キャンプ", "category": "レジャー"},
        {"name": "スキー・スノーボード", "category": "レジャー"},
        {"name": "マリンスポーツ", "category": "レジャー"},
        {"name": "ピクニック", "category": "レジャー"},

        {"name": "フェス・ライブ", "category": "イベント"},
        {"name": "スポーツ観戦", "category": "イベント"},
        {"name": "花火大会", "category": "イベント"},
        {"name": "BBQ", "category": "イベント"},
        {"name": "結婚式参列", "category": "イベント"},
        
        {"name": "サウナ巡り", "category": "趣味・体験"},
        {"name": "絵画スケッチ", "category": "趣味・体験"},
        {"name": "神社仏閣巡り", "category": "趣味・体験"},
        {"name": "ゲーム", "category": "趣味・体験"},

        {"name": "出張", "category": "ビジネス"},
        {"name": "研修・セミナー", "category": "ビジネス"},
        {"name": "学会発表", "category": "ビジネス"},
        {"name": "面接・就活", "category": "ビジネス"},

    ]

    for p in data:
        if not Purpose.query.filter_by(name=p["name"]).first():
           db.session.add(Purpose(name=p["name"], category=p["category"]))
    db.session.commit()

def seed_item():
    data = [
        {"name": "アウター", "category": "衣類", "for_season": "winter"},
        {"name": "歯ブラシ", "category": "生活用品"},
        {"name": "充電ケーブル", "category": "電子機器"},
        {"name": "タオル", "category": "生活用品"},
        {"name": "登山靴", "category": "アウトドア"},
        {"name": "名刺", "category": "ビジネス"},
    ]

    for i in data:
        if not Item.query.filter_by(name=i["name"]).first():
           db.session.add(
               Item(
                   name=i["name"],
                   category=i["category"],
                    for_gender=i.get("for_gender", "all"),
                    for_season=i.get("for_season", "all"),
                    for_weather=i.get("for_weather", "all"),
                    for_transport=i.get("for_transport", "all"),
                    min_days=i.get("min_days"),
                    max_days=i.get("max_days")
               )
           )
    db.session.commit()

def seed_purpose_item():
    data = [
        {"purpose_name": "登山", "item_names":["登山靴"]},
        {"purpose_name": "出張", "item_names": ["充電ケーブル","名刺"]},
    ]

    for check in data:
        purpose = Purpose.query.filter_by(name=check["purpose_name"]).first()
        if not purpose:
            continue
        items = Item.query.filter(Item.name.in_(check["item_names"])).all()

        for item in items:
            if not PurposeItem.query.filter_by(purpose_id=purpose.id, item_id=item.id).first():
                db.session.add(PurposeItem(purpose_id=purpose.id, item_id=item.id))
    
    db.session.commit()

if __name__ == "__main__":
    app = create_app()
    with app.app_context():
        seed_purpose()
        seed_item()
        seed_purpose_item()