import json
from flask import Flask, request
from flask_sqlalchemy import SQLAlchemy

from functions import load_data


app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///:memory:"
app.config['JSON_AS_ASCII'] = False
app.app_context().push()
db = SQLAlchemy(app)


class User(db.Model):
    """
    The class inherits from db.Model and is designed to represent the "users" table when working
    in a database using the Flask-Sqlalchemy framework. Contains a description of the column properties
    and the installed database dependencies.
    """
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    first_name = db.Column(db.String, nullable=False)
    last_name = db.Column(db.String, nullable=False)
    age = db.Column(db.Integer, db.CheckConstraint("age >= 18"))
    email = db.Column(db.String, unique=True)
    phone = db.Column(db.String(12), unique=True)
    role = db.Column(db.String)

    customers = db.relationship('Customer', cascade='save-update, merge, delete')
    executors = db.relationship('Executor', cascade='save-update, merge, delete')


class Customer(db.Model):
    """
    The class inherits from db.Model is auxiliary and is designed to separate users depending on their role
    and represents the "customers" table when working in a database using the Flask-Sqlalchemy framework.
    Contains a description of the column properties and the installed database dependencies.
    """
    __tablename__ = "customers"

    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), primary_key=True)

    orders = db.relationship('Order', cascade='save-update, merge, delete')


class Executor(db.Model):
    """
    The class inherits from db.Model is auxiliary and is designed to separate users depending on their role
    and represents the "executors" table when working in a database using the Flask-Sqlalchemy framework.
    Contains a description of the column properties and the installed database dependencies.
    """
    __tablename__ = "executors"

    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), primary_key=True)

    orders = db.relationship('Order', cascade='save-update, merge, delete')
    offers = db.relationship('Offer', cascade='save-update, merge, delete')


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


db.drop_all()
db.create_all()

# Preparation of initial data for database creation.
users = []
for item in load_data('users.json'):
    users.append(User(id=item['id'], first_name=item['first_name'], last_name=item['last_name'], age=item['age'],
                      email=item['email'], role=item['role'], phone=item['phone']))

db.session.begin()
db.session.add_all(users)

customers = []
for item in User.query.filter(User.role == 'customer').all():
    customers.append(Customer(user_id=item.id))

db.session.add_all(customers)

executors = []
for item in User.query.filter(User.role == 'executor').all():
    executors.append(Executor(user_id=item.id))

db.session.add_all(executors)

orders = []
for item in load_data('orders.json'):
    orders.append(Order(id=item['id'], name=item['name'], description=item['description'],
                        start_date=item['start_date'], end_date=item['end_date'], address=item['address'],
                        price=item['price'], customer_id=item['customer_id'], executor_id=item['executor_id']))

db.session.add_all(orders)

offers = []
for item in load_data('offers.json'):
    offers.append(Offer(id=item['id'], order_id=item['order_id'], executor_id=item['executor_id']))

db.session.add_all(offers)
db.session.commit()


@app.route('/users', methods=['GET', 'POST'])
def get_or_create_users():
    """

    """
    if request.method == 'GET':
        user_list = []
        for item in User.query.all():
            user_list.append({"id": item.id, "first_name": item.first_name, "last_name": item.last_name,
                              "age": item.age, "email": item.email, "role": item.role, "phone": item.phone})
        return json.dumps(user_list)
    elif request.method == 'POST':
        user = request.json
        user_new = User(id=user.get("id"), first_name=user.get("first_name"), last_name=user.get("last_name"),
                        age=user.get("age"), email=user.get("email"), role=user.get("role"), phone=user.get("phone"))
        db.session.add(user_new)

        if user_new.role == "executor":
            executor = Executor(user_id=user_new.id)
            db.session.add(executor)

        elif user_new.role == "customer":
            customer = Customer(user_id=user_new.id)
            db.session.add(customer)

        db.session.commit()
        return json.dumps({"id": user_new.id, "first_name": user_new.first_name, "last_name": user_new.last_name,
                           "age": user_new.age, "email": user_new.email, "role": user_new.role,
                           "phone": user_new.phone})


@app.route('/users/<int:id>', methods=['GET', 'PUT', 'DELETE'])
def get_or_update_or_delete_user(id):
    """

    """
    user = User.query.get(id)

    if request.method == 'GET':
        return json.dumps({"id": user.id, "first_name": user.first_name, "last_name": user.last_name, "age": user.age,
                           "email": user.email, "role": user.role, "phone": user.phone})

    elif request.method == 'PUT':
        user_update = request.json

        user.id = user_update.get('id')
        user.first_name = user_update.get('first_name')
        user.last_name = user_update.get('last_name')
        user.age = user_update.get('age')
        user.email = user_update.get('email')
        user.role = user_update.get('role')
        user.phone = user_update.get('phone')

        db.session.add(user)
        db.session.commit()

        return json.dumps({"id": user.id, "first_name": user.first_name, "last_name": user.last_name, "age": user.age,
                           "email": user.email, "role": user.role, "phone": user.phone})

    elif request.method == 'DELETE':
        db.session.delete(user)
        db.session.commit()

        return json.dumps({"message": "The database object was successfully deleted"})


@app.route('/orders', methods=['GET', 'POST'])
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


@app.route('/orders/<int:id>', methods=['GET', 'PUT', 'DELETE'])
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


@app.route('/offers', methods=['GET', 'POST'])
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


@app.route('/offers/<int:id>', methods=['GET', 'PUT', 'DELETE'])
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


if __name__ == '__main__':

    app.run(debug=True)
