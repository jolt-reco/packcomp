from app import db

# ユーザー
class User(db.Model):
    __tablename__ = "users"
    id = db.Column(db.Integer, primary_key=True)
    user_name = db.Column(db.String, nullable=False)
    email = db.Column(db.String, nullable=False, unique=True)
    password = db.Column(db.String, nullable=False)

    travels = db.relationship("Travel", backref="user", lazy=True)
    bags = db.relationship("Bag", backref="user", lazy=True)
    custom_items = db.relationship("CustomItem", backref="user", lazy=True)
    my_sets = db.relationship("MySet", backref="user", lazy=True)

# トラベル
class Travel(db.Model):
    __tablename__ = "travels"
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    title = db.Column(db.String, nullable=False)
    destination = db.Column(db.String, nullable=False)
    departure_date = db.Column(db.Date, nullable=False)
    return_date = db.Column(db.Date, nullable=False)
    male_count = db.Column(db.Integer, default=1)
    female_count = db.Column(db.Integer, default=0)
    child_count = db.Column(db.Integer, default=0)
    purpose = db.Column(db.String, nullable=False)

# バッグ
class Bag(db.Model):
    __tablename__ = "bags"
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    name = db.Column(db.String, nullable=False)
    length_cm = db.Column(db.Float, nullable=False)
    width_cm = db.Column(db.Float, nullable=False)
    height_cm = db.Column(db.Float, nullable=False)
    volume_l = db.Column(db.Float, nullable=False)
    image_path = db.Column(db.String, nullable=True)
    description = db.Column(db.String, nullable=True)

# アイテム
class Item(db.Model):
    __tablename__ = "items"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    category = db.Column(db.String, nullable=False)
    auto_gen = db.Column(db.Boolean, nullable=False)


# カスタムアイテム
class CustomItem(db.Model):
    __tablename__ = "custom_items"
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    name = db.Column(db.String, nullable=False)
    category = db.Column(db.String, nullable=False)
    size_length_cm = db.Column(db.Float, nullable=True)
    size_width_cm = db.Column(db.Float, nullable=True)
    size_height_cm = db.Column(db.Float, nullable=True)
    image_path = db.Column(db.String, nullable=True)
    note = db.Column(db.String, nullable=True)


# マイセット
class MySet(db.Model):
    __tablename__ = "my_sets"
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    name = db.Column(db.String, nullable=False)


# マイセットアイテム
class MySetItem(db.Model):
    __tablename__ = "my_set_items"
    id = db.Column(db.Integer, primary_key=True)
    my_set_id = db.Column(db.Integer, db.ForeignKey("my_sets.id"), nullable=False)
    item_id = db.Column(db.Integer, db.ForeignKey("items.id"), nullable=True)
    custom_item_id = db.Column(db.Integer, db.ForeignKey("custom_items.id"), nullable=True)
    quantity = db.Column(db.Integer, nullable=False)
    note = db.Column(db.String, nullable=True)


# 旅行アイテム
class TravelItem(db.Model):
    __tablename__ = "travel_items"
    id = db.Column(db.Integer, primary_key=True)
    my_set_item_id = db.Column(db.Integer, db.ForeignKey("my_set_items.id"), nullable=True)
    item_id = db.Column(db.Integer, db.ForeignKey("items.id"), nullable=True)
    custom_item_id = db.Column(db.Integer, db.ForeignKey("custom_items.id"), nullable=True)
    travel_id = db.Column(db.Integer, db.ForeignKey("travels.id"), nullable=False)
    quantity = db.Column(db.Integer, nullable=False)
    note = db.Column(db.String, nullable=True)
    check_flag = db.Column(db.Boolean, nullable=False, default=False)


# パッキングプラン
class PackingPlan(db.Model):
    __tablename__ = "packing_plans"
    id = db.Column(db.Integer, primary_key=True)
    bag_id = db.Column(db.Integer, db.ForeignKey("bags.id"), nullable=False)
    travel_id = db.Column(db.Integer, db.ForeignKey("travels.id"), nullable=False)
    explanation = db.Column(db.String, nullable=False)
    image_path = db.Column(db.String, nullable=True)
