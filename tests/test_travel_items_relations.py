import pytest
from sqlalchemy.exc import IntegrityError
from app.models import User, Travel, Item, CustomItem, MySet, MySetItem, TravelItem
from datetime import date

def test_travel_items_relations(session):
    # データ作成
    user = User(user_name="shichiro", email="shichiro@test.com")
    user.set_password("pass")
    session.add(user)

    travel = Travel(
        user=user,
        title="石川旅行",
        destination="金沢",
        departure_date=date(2025, 9, 20),
        return_date=date(2025, 9, 23)
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

# チェック制約確認
@pytest.mark.skip(reason="PostgreSQL専用のチェック制約なのでSQLiteでは確認できない")
def test_travel_item_check_constraint(session):
    # データ作成
    user = User(user_name="yuji", email="yuji@test.com")
    user.set_password("pass")
    session.add(user)

    travel = Travel(
        user=user,
        title="福岡旅行",
        destination="福岡",
        departure_date=date(2025, 9, 20),
        return_date=date(2025, 9, 23)
    )
    session.add(travel)

    # item, custom_item, my_set_item 全て None にした TravelItem を追加してみる
    travel_item = TravelItem(
        travel=travel,
        quantity=1
        # item, custom_item, my_set_item を全部 None にして制約違反を起こす
    )
    session.add(travel_item)

    # チェック制約で IntegrityError が発生するはず
    with pytest.raises(IntegrityError):
        session.commit()
        session.rollback() 


# 自動持ち物生成ロジックテスト
def auto_generated_travel_items(session, user_with_travel, master_items):
    user, travel = user_with_travel

    # 持ち込みNGアイテムをリストから除外
    if travel.transport == "飛行機":
        usable_items = [ti for ti in master_items if ti.category != "制限:飛行機NG"]
    else:
        usable_items = master_items

    # 宿泊日数計算
    days = (travel.return_date - travel.departure_date).days

    # 衣類抽出→数量補正
    for pickup_item in usable_items:
        if pickup_item.category == "衣類":
            travel_item =TravelItem(
                travel=travel, 
                item=pickup_item, 
                quantity=days
            )
            session.add(travel_item)
    
    # 数量1アイテム抽出
    for pickup_item in usable_items:
        if pickup_item.category in ["必需品", "電子機器", "アメニティ"]:
            travel_item = TravelItem(
                travel=travel,
                item=pickup_item,
                quantity=1
                )
            session.add(travel_item)
    
    # 性別でアイテム抽出
    if travel.female_count > 0:
        for pickup_item in usable_items:
            if pickup_item.category == "性別:女性":
                travel_item = TravelItem(
                    travel=travel,
                    item=pickup_item,
                    quantity=travel.female_count
                )
                session.add(travel_item)
 
    # 子供の有無でアイテム抽出
    if travel.child_count > 0:
        for pickup_item in usable_items:
            if pickup_item.category == "子供":
                travel_item = TravelItem(
                    travel=travel,
                    item=pickup_item,
                    quantity=travel.child_count
                )
                session.add(travel_item)

    session.commit()

# 自動生成結果確認
def test_auto_generated_travel_item(session, user_with_travel, master_items):
    user, travel = user_with_travel
    
    # 自動生成実行
    auto_generated_travel_items(session, user_with_travel, master_items)

    # TravelItemに追加した持ち物をリスト化
    travel_items = travel.travel_items

    # 衣類(3泊分)確認
    socks_item = [ti for ti in travel_items if ti.item.name == "靴下"] 
    assert len(socks_item) == 1
    assert socks_item[0].quantity == 3

    # 数量1アイテム確認
    for name in ["スマホ", "財布", "充電器", "歯ブラシ", "シャンプー"]:
        only_one_item = next(ti for ti in travel_items if ti.item.name == name )
        assert only_one_item.quantity == 1
    
    # 女性向けアイテム確認(個数はfemale_countと同じ)
    female_item = next(ti for ti in travel_items if ti.item.name == "生理用品")
    assert female_item.quantity == travel.female_count

    # 子供向けアイテム確認(個数はchild_countと同じ)
    for name in ["オムツ", "ベビーカー"]:
        child_item = next(ti for ti in travel_items if ti.item.name == name)
        assert child_item.quantity == travel.child_count

    # 飛行機NGアイテムは入っていない
    ng_item = [ti.item.name for ti in travel_items]
    assert "液体シャンプー(100ml以上)" not in ng_item