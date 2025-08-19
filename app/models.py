from app import db

# User
class User(db.Model):
    __tablename__ = "users"
    id = db.Column(db.Integer, primary_key=True)
    user_name = db.Column(db.String, nullable=False)
    email = db.Column(db.String, nullable=False, unique=True)
    password = db.Column(db.String, nullable=False)

    travels = db.relationship("Travel", back_populates="user", cascade="all, delete-orphan")
    bags = db.relationship("Bag", back_populates="user", cascade="all, delete-orphan")
    custom_items = db.relationship("CustomItem", back_populates="user", cascade="all, delete-orphan")
    my_sets = db.relationship("MySet", back_populates="user", cascade="all, delete-orphan")
   
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
    purpose = db.Column(db.String, nullable=False)
    
    user = db.relationship("User", back_populates="travels")
    travel_items = db.relationship("TravelItem", back_populates="travel", cascade="all, delete-orphan")
    packing_plans = db.relationship("PackingPlan", back_populates="travel", cascade="all, delete-orphan")

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
    auto_gen = db.Column(db.Boolean, nullable=False)

    my_set_items = db.relationship("MySetItem", back_populates="item")

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

# MySet
class MySet(db.Model):
    __tablename__ = "my_sets"
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    name = db.Column(db.String, nullable=False)

    user = db.relationship("User", back_populates="my_sets")
    my_set_items = db.relationship("MySetItem", back_populates="my_set", cascade="all, delete-orphan")

# MySetItem
class MySetItem(db.Model):
    __tablename__ = "my_set_items"
    id = db.Column(db.Integer, primary_key=True)
    my_set_id = db.Column(db.Integer, db.ForeignKey("my_sets.id"), nullable=False)
    item_id = db.Column(db.Integer, db.ForeignKey("items.id"), nullable=True)
    custom_item_id = db.Column(db.Integer, db.ForeignKey("custom_items.id"), nullable=True)
    quantity = db.Column(db.Integer, nullable=False)
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
    item = db.relationship("Item")
    custom_item = db.relationship("CustomItem")

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