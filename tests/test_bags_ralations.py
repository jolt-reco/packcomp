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

# cascade処理確認
def test_bag_cascade_delete(session):
    # データ作成
    user = User(user_name="yamagishi", email="yamagishi@test.com", password="pass")
    session.add(user)

    travel = Travel(
        user=user,
        title="長野旅行",
        destination="長野",
        departure_date="2025-09-20",
        return_date="2025-09-23",
        purpose="観光"
    )
    session.add(travel)

    bag = Bag(user=user, name="キャリーバッグ", length_cm=50, width_cm=30, height_cm=20, volume_l=30)
    session.add(bag)

    packing_plan = PackingPlan(bag=bag, travel=travel, explanation="プランA")
    session.add(packing_plan)
    session.commit()

    # Bag 削除
    session.delete(bag)
    session.commit()

    # 関連データが削除されているか確認
    assert session.query(PackingPlan).filter_by(id=packing_plan.id).first() is None