"""Flask forms with validators"""
# Flask imports
from flask_wtf import FlaskForm

# WTForms imports
from wtforms import StringField, IntegerField, SubmitField, BooleanField, SelectField
from wtforms.validators import DataRequired, NumberRange


class NewProduct(FlaskForm):
    product_name = StringField('Product Name', validators=[DataRequired()])
    product_description = StringField('Product Description', validators=[DataRequired()])
    product_sku = StringField('Product SKU')
    product_quantity = IntegerField('Quantity', validators=[NumberRange(min=1, max=1000), DataRequired()])
    product_price = IntegerField('Price', validators=[NumberRange(min=1, max=1000), DataRequired()])
    product_submit = SubmitField('Save Changes')


class NewShop(FlaskForm):
    shop_name = StringField('Shop Name', validators=[DataRequired()])
    shop_location = StringField('Shop Location', validators=[DataRequired()])
    shop_description = StringField('Shop Description')
    shop_active = BooleanField('Is active?')
    shop_submit = SubmitField('Save Changes')


class NewTransaction(FlaskForm):
    product_name = SelectField('Product Name')
    origin = SelectField('Origin Point')
    end = SelectField('End Point')
    product_quantity = IntegerField('Quantity', validators=[NumberRange(min=1, max=1000), DataRequired()])
    transaction_submit = SubmitField('Submit Changes')
