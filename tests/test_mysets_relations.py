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

# cascade処理確認
def test_myset_cascade_delete(session):
    # データ作成
    user = User(user_name="kobori", email="kobori@test.com", password="pass")
    session.add(user)
    session.commit()

    my_set = MySet(user=user, name="出張セット")
    session.add(my_set)

    item = Item(name="名刺入れ", category="仕事")
    session.add(item)

    my_set_item = MySetItem(my_set=my_set, item=item, quantity=1)
    session.add(my_set_item)

    session.commit()

    # MySet 削除
    session.delete(my_set)
    session.commit()

    # 関連データが消えているか確認
    assert session.query(MySetItem).filter_by(id=my_set_item.id).first() is None
