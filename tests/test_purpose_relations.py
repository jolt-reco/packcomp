import pytest
from app import db
from app.models import User, Purpose, Travel, TravelPurpose
from datetime import date

def test_purpose_relations(session):
    
    # データ作成
    user = User(user_name="kuro", email="kuro@test.com")
    user.set_password("pass")
    db.session.add(user)
    db.session.commit()

    beach = Purpose(name="ビーチ")
    hiking = Purpose(name="ハイキング")
    db.session.add_all([beach, hiking])
    db.session.commit()

    # 旅行作成
    travel = Travel(
        user_id=user.id,
        title="沖縄旅行",
        destination="沖縄",
        departure_date=date(2025, 9, 20),
        return_date=date(2025, 9, 23)
    )
    db.session.add(travel)
    db.session.commit()

    # TravelPurpose の紐付け確認
    tp1 = TravelPurpose(travel_id=travel.id, purpose_id=beach.id)
    tp2 = TravelPurpose(travel_id=travel.id, purpose_id=hiking.id)
    db.session.add_all([tp1, tp2])
    db.session.commit()

    # 紐付けされた目的が2件あるか確認
    travel_with_purpose = session.get(Travel, travel.id)
    assert len(travel_with_purpose.travel_purposes) == 2