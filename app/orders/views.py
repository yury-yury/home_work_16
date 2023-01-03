from flask import Blueprint, request
import json

from model import Order, db
from ..offers.model import Offer

orders_blueprint = Blueprint('orders_blueprint', __name__, url_prefix ='/orders')


@orders_blueprint.route('/orders', methods=['GET', 'POST'])
def get_or_create_orders():
    """

    """
    if request.method == 'GET':
        order_list = []
        for item in Order.query.all():
            order_list.append({"id": item.id, "name": item.name, "description": item.description,
                               "start_date": item.start_date, "end_date": item.end_date, "address": item.address,
                               "price": item.price, "customer_id": item.customer_id, "executor_id": item.executor_id})
        return json.dumps(order_list)

    elif request.method == 'POST':
        order = request.json
        order_new = Order(id=order.get("id"), name=order.get("name"), description=order.get("description"),
                          start_date=order.get("start_date"), end_date=order.get("end_date"),
                          address=order.get("address"), price=order.get("price"), customer_id=order.get("customer_id"),
                          executor_id=order.get("executor_id"))
        db.session.add(order_new)

        if order_new.executor_id:
            offer = Offer(order_id=order_new.id, executor_id=order_new.executor_id)
            db.session.add(offer)

        db.session.commit()

        return json.dumps({"id": order.id, "name": order.name, "description": order.description,
                           "start_date": order.start_date, "end_date": order.end_date, "address": order.address,
                           "price": order.price, "customer_id": order.customer_id, "executor_id": order.executor_id})


@orders_blueprint.route('/orders/<int:id>', methods=['GET', 'PUT', 'DELETE'])
def get_or_update_or_delete_order(id):
    """

    """
    order = Order.query.get(id)

    if request.method == 'GET':
        return json.dumps({"id": order.id, "name": order.name, "description": order.description,
                           "start_date": order.start_date, "end_date": order.end_date, "address": order.address,
                           "price": order.price, "customer_id": order.customer_id, "executor_id": order.executor_id})

    elif request.method == 'PUT':
        order_update = request.json

        order.id = order_update.get('id')
        order.name = order_update.get('name')
        order.description = order_update.get('description')
        order.stert_date = order_update.get('start_date')
        order.end_date = order_update.get('end_date')
        order.address = order_update.get('address')
        order.price = order_update.get('price')
        order.customer_id = order_update.get('customer_id')
        order.executor_id = order_update.get('executor')

        db.session.add(order)
        db.session.commit()

        return json.dumps({"id": order.id, "name": order.name, "description": order.description,
                           "start_date": order.start_date, "end_date": order.end_date, "address": order.address,
                           "price": order.price, "customer_id": order.customer_id, "executor_id": order.executor_id})

    elif request.method == 'DELETE':
        db.session.delete(order)
        db.session.commit()

        return json.dumps({"message": "The database object was successfully deleted"})
