import pytest
from app.models import User, MySet, Item, MySetItem

def test_my_sets_relations(session):

    # データ作成
    user = User(user_name="goro", email="goro@test.com", password="pass")
    session.add(user)

    my_set = MySet(user=user, name="ゲームセット")
    session.add(my_set)

    item = Item(name="switch", category="電子機器")
    session.add(item)

    my_set_item = MySetItem(my_set=my_set, item=item, quantity=1)
    session.add(my_set_item)
    session.commit()

    # リレーション確認
    assert my_set_item in my_set.my_set_items
    assert my_set_item.my_set == my_set


