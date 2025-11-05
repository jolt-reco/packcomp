import pytest
from app.models import User, Travel, MySet, MySetItem, TravelItem, CustomItem
from datetime import date

def test_customitems_relations(session):

    # データ作成
    user = User(user_name="Shiro", email="shiro@test.com")
    user.set_password("pass")
    session.add(user)

    custom_item = CustomItem(
        user=user,
        name="歯ブラシ",
        category="アメニティ"
    )
    session.add(custom_item)

    my_set = MySet(user=user, name="洗面用具セット")
    session.add(my_set)

    my_set_item = MySetItem(my_set=my_set, custom_item=custom_item, quantity=1)
    session.add(my_set_item)

    travel = Travel(
        user=user,
        title="北海道旅行",
        destination="札幌",
        departure_date=date(2025, 9, 20),
        return_date=date(2025, 9, 23)
    )
    session.add(travel)

    travel_item = TravelItem(travel=travel, custom_item=custom_item, quantity=1)
    session.add(travel_item)
    
    session.commit()

    # リレーション確認
    # custom_item → my_set_items
    assert my_set_item in custom_item.my_set_items
    assert my_set_item.custom_item == custom_item

    # custom_item → travel_items
    assert travel_item in custom_item.travel_items
    assert travel_item.custom_item == custom_item