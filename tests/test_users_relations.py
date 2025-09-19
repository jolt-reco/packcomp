import pytest
from app.models import User, Travel, Bag, CustomItem, MySet

def test_user_relations(session):

    # データ作成
    user = User(user_name="Taro", email="taro@test.com", password="pass")
    session.add(user)
    session.commit()

    travel = Travel(
        user_id=user.id,
        title="沖縄旅行",
        destination="沖縄",
        departure_date="2025-09-20",
        return_date="2025-09-23",
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
