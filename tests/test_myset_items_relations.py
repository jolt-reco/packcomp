import pytest
from app.models import User, MySet, Item, MySetItem

def test_my_set_items_relations(session):
    # データ作成
    user = User(user_name="rokuro", email="rokuro@test.com", password="pass")
    session.add(user)

    my_set = MySet(user=user, name="防災セット")
    session.add(my_set)

    item = Item(name="懐中電灯", category="防災用品")
    session.add(item)

    my_set_item = MySetItem(my_set=my_set, item=item, quantity=2)
    session.add(my_set_item)
    session.commit()


