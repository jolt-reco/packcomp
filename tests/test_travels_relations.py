import pytest
from app.models import User, Travel, Item, TravelItem, Bag, PackingPlan

def test_travels_relations(session):

    # データ作成
    user = User(user_name="ichiro", email="ichiro@test.com", password="pass")
    travel = Travel(
        title="東京旅行",
        destination="東京",
        departure_date="2025-09-20",
        return_date="2025-09-23",
        purpose="観光"
    )
    user.travels.append(travel)
    session.add(user)    

    item = Item(name="財布", category="貴重品")
    travel_item = TravelItem(travel=travel, item=item, quantity=1)
    session.add(item)
    session.add(travel_item)

    bag=Bag(
        user = user,
        name="キャリーバック",
        length_cm=50,
        width_cm=30,
        height_cm=20,
        volume_l=30
    )
    packing_plan=PackingPlan(
        bag=bag,
        travel=travel,
        explanation="プラン1"
    )
    session.add(bag)
    session.add(packing_plan)
    session.commit()

    # リレーション確認
    # travels → travel_items
    assert travel_item in travel.travel_items
    
    # travel_items → travels
    assert travel_item.travel == travel

    # travel → packing_plans
    assert packing_plan in travel.packing_plans

    # packing_plans → travel
    assert packing_plan.travel == travel