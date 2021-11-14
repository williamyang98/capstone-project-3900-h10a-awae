"""
Routes for basic ecommerce functionalities available to register or unregistered users
This includes browsing and visitng product pages and viewing orders
"""

from flask import json, redirect, request, render_template, url_for, jsonify, abort, session
from flask_login import current_user

from server import app, get_db
from .endpoints import user_bp, api_bp
from .forms import ProductSearchParams, serialize_form

# Product browsing
@user_bp.route('/', methods=["GET", "POST"])
def home():
    with app.app_context():
        db = get_db()
        recommended_products = db.get_random_entries("products", 4)
        # If user has bought at least 10 products
            # Gets last 10 products a user bought
        recent_categories = []
        orders = db.get_entries_by_heading("order2", "user_id", current_user.get_id())
        for order in orders:
            order_item = db.get_entries_by_heading("order2_item", "order2_id", order["id"])
            assert(len(order_item) == 1)
            order_item = order_item[0]
            product = db.get_entry_by_id("products", order_item["product_id"])
            category = product["category"]
            recent_categories.append(category)

        # Else if user has bought 0-9 products
            # Gets last 0-9 products a user bought
            # Randomly fill in remaining products
        # Randomly pick 4 products and get their categories
        # Randomly select a product from each category chosen (unique products)
        # Display the 4 products on home page


        # Aggregate all products and quantity users have bought
        # Display most popular products
        # (potentially) display how much was sold
        popular_items = db.get_random_entries("products", 12)
    
    data = dict(recommended_products=recommended_products, popular_items=popular_items)
    
    return render_template("homepage.html", **data)

@user_bp.route('/products/<string:id>', methods=['GET'])
def product_page(id):
    with app.app_context():
        db = get_db()
        product = db.get_entry_by_id("products", id)
        similar_items = db.get_random_entries("products", 12)
    return render_template('product.html', product=product, similar_items=similar_items)

@user_bp.route('/search', methods=['GET', 'POST'])
def search():
    with app.app_context():
        db = get_db()
        valid_categories = db.get_unique_values("products", "category")
        form = ProductSearchParams()
        dict_sort_by = {
            "price_low_to_high": "unit_price ASC",
            "price_high_to_low": "unit_price DESC"
        }
        sort_by = dict_sort_by[form.sort_type.data]
        products = db.search_product_by_name(form.name.data, form.categories.data, sort_by)
    return render_template('search.html', products=products, categories=valid_categories, form=form)
