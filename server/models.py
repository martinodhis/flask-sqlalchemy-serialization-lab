# server/models.py
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import MetaData
from sqlalchemy.ext.associationproxy import association_proxy
from marshmallow import Schema, fields

# Configure SQLAlchemy to use consistent naming for foreign keys
metadata = MetaData(naming_convention={
    "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
})

# Initialize SQLAlchemy with the metadata
db = SQLAlchemy(metadata=metadata)

# --- MODELS ---

class Review(db.Model):
    """
    Review model: represents a review left by a customer for an item.
    Acts as a join table between Customer and Item.
    """
    __tablename__ = 'reviews'

    id = db.Column(db.Integer, primary_key=True)
    comment = db.Column(db.String)  # The review text
    customer_id = db.Column(db.Integer, db.ForeignKey('customers.id'))  # Foreign key to Customer
    item_id = db.Column(db.Integer, db.ForeignKey('items.id'))  # Foreign key to Item

    # Define relationships to Customer and Item
    customer = db.relationship("Customer", back_populates="reviews")
    item = db.relationship("Item", back_populates="reviews")

    def __repr__(self):
        return f'<Review {self.id}, {self.comment}>'

class Customer(db.Model):
    """
    Customer model: represents a customer who can review items.
    """
    __tablename__ = 'customers'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)  # Customer's name

    # One-to-many relationship: a customer can have many reviews
    reviews = db.relationship("Review", back_populates="customer")
    # Association proxy: allows direct access to items reviewed by the customer
    items = association_proxy('reviews', 'item')

    def __repr__(self):
        return f'<Customer {self.id}, {self.name}>'

class Item(db.Model):
    """
    Item model: represents an item that can be reviewed by customers.
    """
    __tablename__ = 'items'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)  # Item's name
    price = db.Column(db.Float)  # Item's price

    # One-to-many relationship: an item can have many reviews
    reviews = db.relationship("Review", back_populates="item")

    def __repr__(self):
        return f'<Item {self.id}, {self.name}, {self.price}>'

# --- SCHEMAS ---
# Marshmallow schemas for serializing models to JSON

class ReviewSchema(Schema):
    """
    Schema for Review model.
    Serializes review data, including nested customer and item,
    but excludes fields that could cause recursion.
    """
    id = fields.Int()
    comment = fields.Str()
    # Nested serialization for customer and item, excluding their reviews to prevent recursion
    customer = fields.Nested("CustomerSchema", exclude=("reviews", "items"))
    item = fields.Nested("ItemSchema", exclude=("reviews", "customers"))

class CustomerSchema(Schema):
    """
    Schema for Customer model.
    Serializes customer data, including nested reviews and items,
    but excludes fields that could cause recursion.
    """
    id = fields.Int()
    name = fields.Str()
    # Nested serialization for reviews and items, excluding customer to prevent recursion
    reviews = fields.Nested("ReviewSchema", many=True, exclude=("customer",))
    items = fields.Nested("ItemSchema", many=True, exclude=("reviews", "customers"))

class ItemSchema(Schema):
    """
    Schema for Item model.
    Serializes item data, including nested reviews and customers,
    but excludes fields that could cause recursion.
    """
    id = fields.Int()
    name = fields.Str()
    price = fields.Float()
    # Nested serialization for reviews and customers, excluding item to prevent recursion
    reviews = fields.Nested("ReviewSchema", many=True, exclude=("item",))
    customers = fields.Nested("CustomerSchema", many=True, exclude=("reviews", "items"))