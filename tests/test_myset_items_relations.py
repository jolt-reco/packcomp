import pytest
from sqlalchemy.exc import IntegrityError
from app.models import User, MySet, Item, MySetItem, CustomItem

def test_my_set_items_relations(session):
    # データ作成
    user = User(user_name="rokuro", email="rokuro@test.com")
    user.set_password("pass")
    session.add(user)

    my_set = MySet(user=user, name="防災セット")
    session.add(my_set)

    item = Item(name="懐中電灯", category="防災用品")
    session.add(item)

    my_set_item = MySetItem(my_set=my_set, item=item, quantity=2)
    session.add(my_set_item)
    session.commit()

@pytest.mark.skip(reason="PostgreSQL専用の部分的ユニーク制約なのでSQLiteでは確認できない")
# 部分的ユニーク制約確認
def test_my_set_item_unique_constraint(session):
    # データ作成
    user = User(user_name="kuro", email="kuro@test.com")
    user.set_password("pass")
    session.add(user)

    my_set = MySet(user=user, name="旅行セット")
    item = Item(name="リュック", category="バッグ")
    custom_item = CustomItem(user=user, name="折りたたみ傘", category="雨具")

    session.add_all([my_set, item, custom_item])
    session.commit()

    # 重複していない最初の作成はOK
    msi1 = MySetItem(my_set=my_set, item=item, quantity=1)
    msi2 = MySetItem(my_set=my_set, custom_item=custom_item, quantity=1)
    session.add_all([msi1, msi2])
    session.commit()

    # item_id + my_set_id が同じで作ると IntegrityError
    duplicate_item = MySetItem(my_set=my_set, item=item, quantity=2)
    session.add(duplicate_item)
    with pytest.raises(IntegrityError):
        session.commit()
        session.rollback()

    # custom_item_id + my_set_id が同じで作ると IntegrityError
    duplicate_custom_item = MySetItem(my_set=my_set, custom_item=custom_item, quantity=2)
    session.add(duplicate_custom_item)
    with pytest.raises(IntegrityError):
        session.commit()
        session.rollback()
