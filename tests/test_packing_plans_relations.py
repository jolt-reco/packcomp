import pytest
from datetime import date
from app.models import User, Bag, Travel, PackingPlan

def test_packing_plans_relations(session):
    # データ作成
    user = User(user_name="hachiaro", email="hachiro@test.com")
    user.set_password("pass")
    session.add(user)

    bag = Bag(
        user=user,
        name="マウンテンバッグ",
        length_cm=55.0,
        width_cm=35.0,
        height_cm=25.0,
        volume_l=40.0
    )
    session.add(bag)

    travel = Travel(
        user=user,
        title="海外旅行",
        destination="韓国",
        departure_date=date(2025, 9, 20),
        return_date=date(2025, 9, 23)
    )
    session.add(travel)

    plan = PackingPlan(
        bag=bag,
        travel=travel,
        explanation="服・充電器をバッグに詰めるプラン"
    )
    session.add(plan)
    session.commit()

