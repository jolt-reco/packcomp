import pytest
from app.models import User, Travel, Item, TravelItem, MySet, MySetItem
from datetime import date

def test_items_relations(session):

    # データ作成
    user = User(user_name="Saburo", email="saburo@test.com", password="pass")
    session.add(user)

    travel = Travel(
        user=user,
        title="大阪旅行",
        destination="大阪",
        departure_date=date(2025, 9, 20),
        return_date=date(2025, 9, 23),
        purpose="観光"
    )

    item = Item(name="胃薬", category="薬")
    session.add(item)

    my_set = MySet(user=user, name="旅行セット1")
    session.add(my_set)

    my_set_item = MySetItem(my_set=my_set, item=item, quantity=1)
    session.add(my_set_item)

    travel_item = TravelItem(
        my_set_item=my_set_item, 
        item=item, 
        travel=travel, 
        quantity=1
    )
    session.add(travel_item)
    session.commit()

    # リレーション確認
    # Item → MySetItem
    assert my_set_item in item.my_set_items
    assert my_set_item.item == item

