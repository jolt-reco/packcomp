import pytest
from app import create_app, db
from app.models import Item,User,Travel
from datetime import date

@pytest.fixture
def app():
    app = create_app("testing")
    with app.app_context():
        db.create_all()
        yield app
        db.session.remove()
        db.drop_all()

@pytest.fixture
def session(app):
    with app.app_context():
        yield db.session

# 自動生成ロジックテスト用
@pytest.fixture
def user_with_travel(session):
    user = User(
        user_name="test",
        email="test@example.com",
        password="pass"
    )
    session.add(user)
    session.commit()

    travel = Travel(
        user=user,
        title="海外旅行",
        destination="ハワイ",   # 海外
        departure_date=date(2025, 9, 20),
        return_date=date(2025, 9, 23),
        purpose="海",          # 海水浴目的
        transport="飛行機",     # 飛行機移動
        female_count=1,        # 女性1人
        child_count=1            # 子供連れ
    )
    session.add(travel)
    session.commit()

    return user, travel

# 簡易テスト用マスターアイテム
@pytest.fixture
def master_items(session):
    items = [
        # 基本必須
        Item(name="スマホ", category="必需品"),
        Item(name="財布", category="必需品"),
        Item(name="充電器", category="電子機器"),

        # 衣類（日数で増える）
        Item(name="下着", category="衣類"),
        Item(name="靴下", category="衣類"),

        # アメニティ
        Item(name="歯ブラシ", category="アメニティ"),
        Item(name="シャンプー", category="アメニティ"),

        # 性別
        Item(name="生理用品", category="性別:女性"),
        Item(name="髭剃り", category="性別:男性"),

        # 子供
        Item(name="オムツ", category="子供"),
        Item(name="ベビーカー", category="子供"),

        # 目的地
        Item(name="パスポート", category="海外"),
        Item(name="変換プラグ", category="海外"),

        # 目的
        Item(name="水着", category="目的:海"),
        Item(name="スーツ", category="目的:ビジネス"),
        Item(name="登山靴", category="目的:登山"),

        # 交通手段
        Item(name="液体シャンプー(100ml以上)", category="制限:飛行機NG"),

        # 季節・天候
        Item(name="コート", category="冬"),
        Item(name="日焼け止め", category="夏"),
        Item(name="折りたたみ傘", category="雨"),
    ]
    session.add_all(items)
    session.commit()
    return items
