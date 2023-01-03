from home_work_16.app.database import db, load_data
from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship



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


users = []
for item in load_data('data/users.json'):
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
db.session.commit()
