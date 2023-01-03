from ..database import db, load_data

class Order(db.Model):
    """
    The class inherits from db.Model and is designed to represent the "orders" table when working
    in a database using the Flask-Sqlalchemy framework. Contains a description of the column properties
    and the installed database dependencies.
    """
    __tablename__ = "orders"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String, nullable=False)
    description = db.Column(db.Text)
    start_date = db.Column(db.String())
    end_date = db.Column(db.String())
    address = db.Column(db.String)
    price = db.Column(db.Integer)
    customer_id = db.Column(db.Integer, db.ForeignKey("customers.user_id"))
    executor_id = db.Column(db.Integer, db.ForeignKey("executors.user_id"))

    offers = db.relationship('Offer', cascade='save-update, merge, delete')


orders = []
for item in load_data('data/orders.json'):
    orders.append(Order(id=item['id'], name=item['name'], description=item['description'],
                        start_date=item['start_date'], end_date=item['end_date'], address=item['address'],
                        price=item['price'], customer_id=item['customer_id'], executor_id=item['executor_id']))

db.session.add_all(orders)
db.session.commit()
