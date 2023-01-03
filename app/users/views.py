from flask import Blueprint, request
import json

from model import User, Customer, Executor, db


users_blueprint = Blueprint('users_blueprint', __name__, url_prefix='/users')


@users_blueprint.route('/users', methods=['GET', 'POST'])
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


@users_blueprint.route('/users/<int:id>', methods=['GET', 'PUT', 'DELETE'])
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
