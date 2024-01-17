#!/usr/bin/env python3

from flask import Flask, jsonify, make_response
from flask_migrate import Migrate
from models import db, Bakery, BakedGood

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.json.compact = False

migrate = Migrate(app, db)

db.init_app(app)

@app.route('/')
def index():
    return '<h1>Bakery GET API</h1>'

@app.route('/bakeries')
def get_all_bakeries():
    bakeries = Bakery.query.all()
    bakery_list = [{"id": bakery.id, "name": bakery.name, "created_at": str(bakery.created_at)} for bakery in bakeries]

    response = make_response(jsonify(bakery_list), 200)
    response.headers['Content-Type'] = 'application/json'

    return response

@app.route('/bakeries/<int:id>')
def get_bakery_by_id(id):
    bakery = Bakery.query.get(id)
    if bakery:
        baked_goods = BakedGood.query.filter_by(bakery_id=id).all()
        bakery_data = {"id": bakery.id, "name": bakery.name, "created_at": str(bakery.created_at),
                       "baked_goods": [{"id": good.id, "name": good.name, "price": good.price, "created_at": str(good.created_at)} for good in baked_goods]}

        response = make_response(jsonify(bakery_data), 200)
        response.headers['Content-Type'] = 'application/json'

        return response

    return make_response(jsonify({"message": "Bakery not found"}), 404)

@app.route('/baked_goods/by_price')
def baked_goods_by_price():
    baked_goods = BakedGood.query.order_by(BakedGood.price.desc()).all()
    baked_goods_list = [{"id": good.id, "name": good.name, "price": good.price, "created_at": str(good.created_at)} for good in baked_goods]

    response = make_response(jsonify(baked_goods_list), 200)
    response.headers['Content-Type'] = 'application/json'

    return response

@app.route('/baked_goods/most_expensive')
def most_expensive_baked_good():
    most_expensive_good = BakedGood.query.order_by(BakedGood.price.desc()).first()

    if most_expensive_good:
        baked_good_data = {"id": most_expensive_good.id, "name": most_expensive_good.name, "price": most_expensive_good.price,
                           "created_at": str(most_expensive_good.created_at)}

        response = make_response(jsonify(baked_good_data), 200)
        response.headers['Content-Type'] = 'application/json'

        return response

    return make_response(jsonify({"message": "No baked goods found"}), 404)

if __name__ == '__main__':
    app.run(port=5565, debug=True)
