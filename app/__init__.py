from flask import Flask
from .database import db


def create_app():
    app = Flask(__name__)
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///:memory:"
    app.config['JSON_AS_ASCII'] = False
    app.app_context().push()
    db.init_app(app)
    db.create_all()

    from users.views import users_blueprint
    from orders.views import orders_blueprint
    from offers.views import offers_blueprint

    app.register_blueprint(users_blueprint)
    app.register_blueprint(orders_blueprint)
    app.register_blueprint(offers_blueprint)

    return app
