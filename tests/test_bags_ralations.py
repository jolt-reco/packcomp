import pytest
from app.models import User, Bag, Travel, PackingPlan

def test_bags_relations(session):

    # データ作成
    user = User(user_name="Jiro", email="jiro@test.com", password="pass")
    session.add(user)

    bag = Bag(
        user=user,
        name="ショルダーバッグ",
        length_cm=55,
        width_cm=35,
        height_cm=25,
        volume_l=40
    )
    session.add(bag)

    travel = Travel(
        user=user,
        title="京都旅行",
        destination="京都",
        departure_date="2025-09-20",
        return_date="2025-09-23",
        purpose="観光"
    )
    session.add(travel)

    plan = PackingPlan(bag=bag, travel=travel, explanation="プラン2")
    session.add(plan)

    session.commit()

    # リレーション確認
    # bag → packing_plan
    assert plan in bag.packing_plans

    # packing_plan → bag
    assert plan.bag == bag