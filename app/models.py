from app import db
from sqlalchemy import CheckConstraint
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash

# User
class User(UserMixin, db.Model):
    __tablename__ = "users"
    id = db.Column(db.Integer, primary_key=True)
    user_name = db.Column(db.String, nullable=False)
    email = db.Column(db.String, nullable=False, unique=True)
    password_hash = db.Column(db.String, nullable=False)

    travels = db.relationship("Travel", back_populates="user", cascade="all, delete-orphan")
    bags = db.relationship("Bag", back_populates="user", cascade="all, delete-orphan")
    custom_items = db.relationship("CustomItem", back_populates="user", cascade="all, delete-orphan")
    my_sets = db.relationship("MySet", back_populates="user", cascade="all, delete-orphan")

    # パスワード設定用メソッド
    def set_password(self, password):
        self.password_hash = generate_password_hash(password)
    
    # 照合用メソッド
    def check_password(self, password):
        return check_password_hash(self.password_hash, password)
   
# Travel
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
    transport = db.Column(db.String, nullable=True)
    weather_data = db.Column(db.JSON, nullable=True)
    weather_last_update = db.Column(db.DateTime, nullable=True)
    
    user = db.relationship("User", back_populates="travels")
    travel_items = db.relationship("TravelItem", back_populates="travel", cascade="all, delete-orphan")
    travel_purposes = db.relationship("TravelPurpose", back_populates="travel", cascade="all, delete-orphan")
    packing_plans = db.relationship("PackingPlan", back_populates="travel", cascade="all, delete-orphan")

class Purpose(db.Model):
    __tablename__ = "purposes"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False, unique=True)
    category = db.Column(db.String, nullable=False) 

    travel_purposes = db.relationship("TravelPurpose", back_populates="purpose",cascade="all, delete-orphan")
    purpose_items = db.relationship("PurposeItem", back_populates="purpose",cascade="all, delete-orphan")

# TravelPupose
class TravelPurpose(db.Model):
    __tablename__ = "travel_purposes"
    travel_id = db.Column(db.Integer, db.ForeignKey("travels.id"), primary_key=True)
    purpose_id = db.Column(db.Integer, db.ForeignKey("purposes.id"), primary_key=True)

    travel = db.relationship("Travel", back_populates="travel_purposes")
    purpose = db.relationship("Purpose", back_populates="travel_purposes")

# Bag
class Bag(db.Model):
    __tablename__ = "bags"
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    name = db.Column(db.String, nullable=False)
    length_cm = db.Column(db.Float, nullable=False)
    width_cm = db.Column(db.Float, nullable=False)
    height_cm = db.Column(db.Float, nullable=False)
    volume_l = db.Column(db.Float, nullable=False)
    image_path = db.Column(db.String, nullable=True)
    description = db.Column(db.String, nullable=True)

    user = db.relationship("User", back_populates="bags")
    packing_plans = db.relationship("PackingPlan", back_populates="bag", cascade="all, delete-orphan")

# Item
class Item(db.Model):
    __tablename__ = "items"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    category = db.Column(db.String, nullable=False)
    for_gender = db.Column(db.String, nullable=False, default="all")
    for_season = db.Column(db.String, nullable=False, default="all")
    for_weather = db.Column(db.String, default="all")
    for_transport = db.Column(db.String, nullable=False, default="all")
    min_days = db.Column(db.Integer, nullable=True)
    max_days = db.Column(db.Integer, nullable=True)

    my_set_items = db.relationship("MySetItem", back_populates="item")
    travel_items = db.relationship("TravelItem", back_populates="item")
    purpose_items = db.relationship("PurposeItem", back_populates="item",cascade="all, delete-orphan")

# PurposeItem
class PurposeItem(db.Model):
    __tablename__ = "purpose_items"
    purpose_id = db.Column(db.Integer, db.ForeignKey("purposes.id"), primary_key=True)
    item_id = db.Column(db.Integer, db.ForeignKey("items.id"), primary_key=True)
    
    purpose = db.relationship("Purpose", back_populates="purpose_items")
    item = db.relationship("Item", back_populates="purpose_items")

# CustomItem
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
    
    user = db.relationship("User", back_populates="custom_items")
    my_set_items = db.relationship("MySetItem", back_populates="custom_item")
    travel_items = db.relationship("TravelItem", back_populates="custom_item")

# MySet
class MySet(db.Model):
    __tablename__ = "my_sets"
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    name = db.Column(db.String, nullable=False)

    user = db.relationship("User", back_populates="my_sets")
    my_set_items = db.relationship("MySetItem", back_populates="my_set", cascade="all, delete-orphan")

# MySetItem
# item_id / custom_item_id の部分ユニーク制約はマイグレーションで作成
class MySetItem(db.Model):
    __tablename__ = "my_set_items"
    id = db.Column(db.Integer, primary_key=True)
    my_set_id = db.Column(db.Integer, db.ForeignKey("my_sets.id"), nullable=False)
    item_id = db.Column(db.Integer, db.ForeignKey("items.id"), nullable=True)
    custom_item_id = db.Column(db.Integer, db.ForeignKey("custom_items.id"), nullable=True)
    note = db.Column(db.String, nullable=True)

    my_set = db.relationship("MySet", back_populates="my_set_items")
    item = db.relationship("Item", back_populates="my_set_items")
    custom_item = db.relationship("CustomItem", back_populates="my_set_items")
    travel_items = db.relationship("TravelItem", back_populates="my_set_item")

# TravelItem
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

    travel = db.relationship("Travel", back_populates="travel_items")
    my_set_item = db.relationship("MySetItem", back_populates="travel_items")
    item = db.relationship("Item", back_populates="travel_items")
    custom_item = db.relationship("CustomItem", back_populates="travel_items")

    __table_args__ = (
        CheckConstraint(
            "(item_id IS NOT NULL OR custom_item_id IS NOT NULL OR my_set_item_id IS NOT NULL)",
            name="check_travelitems_not_all_null"
        ),
    )

# PackingPlan
class PackingPlan(db.Model):
    __tablename__ = "packing_plans"
    id = db.Column(db.Integer, primary_key=True)
    bag_id = db.Column(db.Integer, db.ForeignKey("bags.id"), nullable=False)
    travel_id = db.Column(db.Integer, db.ForeignKey("travels.id"), nullable=False)
    explanation = db.Column(db.String, nullable=False)
    image_path = db.Column(db.String, nullable=True)

    bag = db.relationship("Bag", back_populates="packing_plans")
    travel = db.relationship("Travel", back_populates="packing_plans")