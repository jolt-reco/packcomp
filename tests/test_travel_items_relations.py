import pytest
from app.models import User, Travel, Item, CustomItem, MySet, MySetItem, TravelItem

def test_travel_items_relations(session):
    # データ作成
    user = User(user_name="shichiro", email="shichiro@test.com", password="pass")
    session.add(user)

    travel = Travel(
        user=user,
        title="石川旅行",
        destination="金沢",
        departure_date="2025-09-20",
        return_date="2025-09-23",
        purpose="観光"
    )
    session.add(travel)

    item = Item(name="ノートPC", category="電子機器")
    session.add(item)

    custom_item = CustomItem(user=user, name="折りたたみ傘", category="雨具")
    session.add(custom_item)

    my_set = MySet(user=user, name="雨対策セット")
    session.add(my_set)

    my_set_item = MySetItem(my_set=my_set, custom_item=custom_item, quantity=1)
    session.add(my_set_item)

    travel_item1 = TravelItem(travel=travel, item=item, quantity=1)
    travel_item2 = TravelItem(travel=travel, custom_item=custom_item, quantity=1)
    travel_item3 = TravelItem(travel=travel, my_set_item=my_set_item, quantity=1)
    session.add_all([travel_item1, travel_item2, travel_item3])
    session.commit()

    # リレーション確認
    # TravelItem → Item/CustomItem/MySetItem
    assert travel_item1.item == item
    assert travel_item2.custom_item == custom_item
    assert travel_item3.my_set_item == my_set_item

    # Item/CustomItem/MySetItem → TravelItem
    assert travel_item1 in item.travel_items
    assert travel_item2 in custom_item.travel_items
    assert travel_item3 in my_set_item.travel_items
