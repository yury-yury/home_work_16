from ..database import db


class Offer(db.Model):
    """
    The class inherits from db.Model and is designed to represent the "offers" table when working
    in a database using the Flask-Sqlalchemy framework. Contains a description of the column properties
    and the installed database dependencies.
    """
    __tablename__ = "offers"

    id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    order_id = db.Column(db.Integer, db.ForeignKey("orders.id"))
    executor_id = db.Column(db.Integer, db.ForeignKey("executors.user_id"))


offers = []
for item in load_data('data/offers.json'):
    offers.append(Offer(id=item['id'], order_id=item['order_id'], executor_id=item['executor_id']))

db.session.add_all(offers)
db.session.commit()