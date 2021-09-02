"""Models for Cargamos® Project"""
from .app import db


class Shop(db.Model):
    __tablename__ = 'shops'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80))
    description = db.Column(db.String(500))
    direction = db.Column(db.String(250))
    active = db.Column(db.Boolean(), default=True)
    created_at = db.Column(db.DateTime, server_default=db.func.now(), nullable=False)
    modified_at = db.Column(db.DateTime, server_default=db.func.now(), server_onupdate=db.func.now(), nullable=False)

    def __repr__(self):
        return f"<Shop {self.name}>"


class Product(db.Model):
    __tablename__ = 'products'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String())
    description = db.Column(db.String(500))
    price = db.Column(db.Integer)
    sku = db.Column(db.String())
    quantity = db.Column(db.Integer)
    created_at = db.Column(db.DateTime, server_default=db.func.now(), nullable=False)
    modified_at = db.Column(db.DateTime, server_default=db.func.now(), server_onupdate=db.func.now(), nullable=False)

    def __repr__(self):
        return f"<Product {self.name}>"


class Transaction(db.Model):
    __tablename__ = 'transactions'

    id = db.Column(db.Integer, primary_key=True)
    created_at = db.Column(db.DateTime, server_default=db.func.now())
    origin = db.Column(db.String(20), nullable=False)
    end = db.Column(db.String(20), nullable=False)
    product_name = db.Column(db.String(20), nullable=False)
    product_quantity = db.Column(db.Integer, nullable=False)
    modified = db.Column(db.DateTime, server_default=db.func.now(), nullable=False)

    def __repr__(self):
        return f"<Transaction where origin: {self.origin}, ends: {self.end}. By the product: {self.product_name}>"


class Holder(db.Model):
    __tablename__ = 'holder'

    id = db.Column(db.Integer, primary_key=True)
    product_name = db.Column(db.String(20), nullable=False)
    shop_name = db.Column(db.String(20), nullable=False)
    quantity = db.Column(db.Integer, nullable=False)

    def __repr__(self):
        return f"<Holder got: {self.product_name}, in shop: {self.shop_name}. By the quantity: {self.quantity}>"
