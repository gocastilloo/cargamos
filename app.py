"""App file for Cargamos® app"""
# Flask
from flask import Flask, render_template, make_response, request, flash, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
# App imports
from .forms import NewProduct, NewShop, NewTransaction
# SQLAlchemy
from sqlalchemy.exc import IntegrityError
# Utils
from datetime import datetime
import pdb
from . import create_app

app = create_app()
db = SQLAlchemy()
from .models import *
db.init_app(app)


@app.route('/home')
def admin():
    shop = Shop.query.all()
    products = Product.query.all()
    headers = {'Content-Type': 'text/html'}
    return make_response(render_template('admin.html', shop=shop, products=products), 200, headers)


@app.route('/shop', methods=['GET', 'POST'])
def shop():
    new_shop = NewShop()
    shops = Shop.query.all()
    if new_shop.validate_on_submit():
        shop = Shop(name=new_shop.shop_name.data,
                    direction=new_shop.shop_location.data,
                    description=new_shop.shop_description.data,
                    active=new_shop.shop_active.data
                    )
        db.session.add(shop)
        try:
            db.session.commit()
            flash(f'Your Shop {new_shop.shop_name.data} has been added!', 'success')
            return redirect('/shop')
        except IntegrityError:
            db.session.rollback()
            flash(f'This shop already exists', 'danger')
            return redirect('/shop')
    headers = {'Content-Type': 'text/html'}
    return make_response(render_template('store_detail.html', shop=shops, form=new_shop), 200, headers)


@app.route('/products', methods=['GET', 'POST'])
def product():
    new_product = NewProduct()
    products = Product.query.all()
    if new_product.validate_on_submit():
        product = Product(name=new_product.product_name.data,
                          description=new_product.product_description.data,
                          sku=new_product.product_sku.data,
                          price=new_product.product_price.data,
                          quantity=new_product.product_quantity.data
                          )
        db.session.add(product)
        try:
            db.session.commit()
            flash(f'Your product {new_product.product_name.data} has been added!', 'success')
            return redirect('/products')
        except IntegrityError:
            db.session.rollback()
            flash(f'This product already exists', 'danger')
            return redirect('/products')
    headers = {'Content-Type': 'text/html'}
    return make_response(render_template('product_detail.html', products=products, form=new_product), 200, headers)


@app.route('/transactions', methods=['GET', 'POST'])
def transactions():
    product_list = []
    shop_list = []
    new_transaction = NewTransaction()
    products = Product.query.all()
    transactions = Transaction.query.all()
    exist = bool(Transaction.query.all())
    if exist is False:
        flash('Add a new transaction', 'danger')

    # Choices for each product
    product_choices = Product.query.with_entities(Product.name).all()
    product_list += product_choices
    new_transaction.product_name.choices = product_list

    # Choices for each store
    shop_choices = Shop.query.with_entities(Shop.name).all()
    shop_list += shop_choices
    new_transaction.origin.choices = shop_list
    new_transaction.end.choices = shop_list

    if new_transaction.validate_on_submit() and request.method == 'POST':
        timestamp = datetime.now()
        validator = transaction_review(new_transaction.origin.data,
                                       new_transaction.end.data,
                                       new_transaction.product_name.data,
                                       new_transaction.product_quantity.data)
        if validator == 'Same point':
            flash('Try again, origin and end must be different', 'danger')
        elif validator is False:
            flash('Try again, quantity must be lower than existed', 'danger')
        else:
            transaction = Transaction(
                modified=timestamp,
                origin=new_transaction.origin.data,
                end=new_transaction.end.data,
                product_name=new_transaction.product_name.data,
                product_quantity=new_transaction.product_quantity.data
            )
            db.session.add(transaction)
            db.session.commit()
            flash(f'Your transaction has been added!', 'success')
            return redirect('/transactions')

    headers = {'Content-Type': 'text/html'}
    return make_response(render_template(
        'transaction.html',
        transactions=transactions,
        form=new_transaction), 200, headers)


def transaction_review(origin, end, product_name, quantity):
    if origin == end:
        return 'Same point'
    elif origin == 'Warehouse' and end != 'Warehouse':
        product = Product.query.filter_by(product_name=product_name).first()
        if product.prod_qty >= quantity:
            product.prod_qty -= quantity
            hold = Holder.query.filter_by(shop_name=origin, product_name=product_name).first()
            a = str(hold)
            if a == 'None':
                new = Holder(product_name=product_name,
                             shop_name=end,
                             quantity=quantity)
                db.session.add(new)
            else:
                hold.quantity += quantity
            db.session.commit()
        else:
            return False
    elif end == 'Warehouse' and origin != 'Warehouse':
        hold = Holder.query.filter_by(shop_name=origin, product_name=product_name).first()
        a = str(hold)
        if a == 'None':
            return 'no prod'
        else:
            if hold.quantity >= quantity:
                prodq = Product.query.filter_by(product_name=product_name).first()
                prodq.prod_qty = prodq.prod_qty + quantity
                hold.quantity -= quantity
                db.session.commit()
            else:
                return False

    else:
        bl = Holder.query.filter_by(shop_name=origin, product_name=product_name).first()
        a = str(bl)
        if a == 'None':
            return 'no prod'

        elif (bl.quantity - 100) > quantity:
            bal = Holder.query.filter_by(shop_name=end, product_name=product_name).first()
            a = str(bal)
            if a == 'None':
                new = Holder(product_name=product_name, shop_name=end, quantity=quantity)
                db.session.add(new)
                bl = Holder.query.filter_by(shop_name=origin, product_name=product_name).first()
                bl.quantity -= quantity
                db.session.commit()
            else:
                    bal.quantity += quantity
                    bl = Holder.query.filter_by(shop_name=origin, product_name=product_name).first()
                    bl.quantity -= quantity
                    db.session.commit()
        else:
            return False


if __name__ == '__main__':
    app.run(debug=True)
