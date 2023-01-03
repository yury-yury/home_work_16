from flask import Blueprint, request
import json

from model import Offer, db

offers_blueprint = Blueprint('offers_blueprint', __name__, url_prefix ='/offers')


@offers_blueprint.route('/offers', methods=['GET', 'POST'])
def get_or_create_offers():
    """

    """
    if request.method == 'GET':
        offers_list = []
        for item in Offer.query.all():
            offers_list.append({"id": item.id, "order_id": item.order_id, "executor_id": item.executor_id})
        return json.dumps(offers_list)

    elif request.method == 'POST':
        offer = request.json

        offer_new = Offer(id=offer.get("id"), order_id=offer.get("order_id"), executor_id=offer.get("executor_id"))
        db.session.add(offer_new)

        db.session.commit()

        return json.dumps({"id": offer.id, "order_id": offer.order_id, "executor_id": offer.executor_id})


@offers_blueprint.route('/offers/<int:id>', methods=['GET', 'PUT', 'DELETE'])
def get_offer(id):
    """

    """
    offer = Offer.query.get(id)

    if request.method == 'GET':

        return json.dumps({"id": offer.id, "order_id": offer.order_id, "executor_id": offer.executor_id})

    elif request.method == 'PUT':

        offer_update = request.json

        offer.id = offer_update.get("id")
        offer.order_id = offer_update.get("order_id")
        offer.executor_id = offer_update.get("executor_id")

        db.session.add(offer)
        db.session.commit()

        return json.dumps({"id": offer.id, "order_id": offer.order_id, "executor_id": offer.executor_id})

    elif request.method == 'DELETE':

        db.session.delete(offer)
        db.session.commit()

        return json.dumps({"message": "The database object was successfully deleted"})
