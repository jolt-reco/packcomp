from app import create_app, db
from app.models import Purpose

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

if __name__ == "__main__":
    app = create_app()
    with app.app_context():
        seed_purpose()

