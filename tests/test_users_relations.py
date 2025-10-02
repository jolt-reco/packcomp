import pytest
from sqlalchemy.exc import IntegrityError
from app.models import User, Travel, Bag, CustomItem, MySet
from datetime import date

def test_user_relations(session):

    # データ作成
    user = User(user_name="Taro", email="taro@test.com", password="pass")
    session.add(user)
    session.commit()

    travel = Travel(
        user_id=user.id,
        title="沖縄旅行",
        destination="沖縄",
        departure_date=date(2025, 9, 20),
        return_date=date(2025, 9, 23),
        purpose="観光"
    )
    session.add(travel)

    bag = Bag(
        user_id=user.id,
        name="バックパック",
        length_cm=50,
        width_cm=30,
        height_cm=20,
        volume_l=30
    )
    session.add(bag)

    custom_item = CustomItem(
        user_id=user.id,
        name="シェーバー",
        category="アメニティ"
    )
    session.add(custom_item)

    my_set = MySet(
        user_id=user.id,
        name="海セット"
    )
    session.add(my_set)

    session.commit()

    #　リレーション確認
    # user → travels
    assert len(user.travels) == 1
    assert user.travels[0].destination == "沖縄"

    # travel → user
    assert travel.user.id == user.id

    # user → bags
    assert len(user.bags) == 1
    assert user.bags[0].name == "バックパック"

    # bag → user
    assert bag.user.id == user.id

    # user → custom_items
    assert len(user.custom_items) == 1
    assert user.custom_items[0].name == "シェーバー"

    # custom_item → user
    assert custom_item.user.id == user.id

    # user → my_sets
    assert len(user.my_sets) == 1
    assert user.my_sets[0].name == "海セット"

    # my_set → user
    assert my_set.user.id == user.id

# メールアドレス重複テスト(重複してたらpass)
def test_user_email_unique(session):
    user1 = User(user_name="asou", email="asou@test.com", password="pass")
    user2 = User(user_name="yamaji", email="asou@test.com", password="pass")
    session.add_all([user1, user2])
    with pytest.raises(IntegrityError):
        session.commit()

# cascade処理確認
def test_user_cascade_delete(session):
    user = User(user_name="hoshi", email="hoshi@test.com", password="pass")
    session.add(user)
    session.commit()

    # 関連データを作成
    travel = Travel(
        user=user,
        title="静岡旅行",
        destination="浜松",
        departure_date="2025-09-20",
        return_date="2025-09-25",
        purpose="観光"
    )
    bag = Bag(user=user, name="スーツケース", length_cm=50, width_cm=30, height_cm=70, volume_l=80)
    custom_item = CustomItem(user=user, name="一眼レフカメラ", category="電子機器")
    my_set = MySet(user=user, name="カメラセット")

    session.add_all([travel, bag, custom_item, my_set])
    session.commit()

    # User 削除
    session.delete(user)
    session.commit()

    # 関連データが消えているか確認
    assert session.query(Travel).filter_by(id=travel.id).first() is None
    assert session.query(Bag).filter_by(id=bag.id).first() is None
    assert session.query(CustomItem).filter_by(id=custom_item.id).first() is None
    assert session.query(MySet).filter_by(id=my_set.id).first() is None