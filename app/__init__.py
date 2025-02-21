from flask import Flask,request,make_response
from config import config
from extensions import db, jwt, bcrypt, migrate
from app.auth.models import User
from app.product.models import Product
from app.warehouse.models import Inventory
from app.auth import auth_bp,routes
from app.product import product_bp,routes
from app.warehouse import warehouse_bp,routes
from app.stock import stock_bp,routes
import logging



def create_app():
    
    app = Flask(__name__)

    app.config.from_object(config())


    db.init_app(app)

    jwt.init_app(app)

    bcrypt.init_app(app)

    migrate.init_app(app,db)

    app.register_blueprint(auth_bp)
    app.register_blueprint(product_bp)
    app.register_blueprint(warehouse_bp)
    app.register_blueprint(stock_bp)

    handler = logging.FileHandler("app.log","a")
    handler.setLevel(logging.DEBUG)
    handler.setFormatter(logging.Formatter("%(asctime)s %(levelname)s %(message)s"))
    app.logger.addHandler(handler)
    app.logger.setLevel(logging.DEBUG)
    app.logger.removeHandler(app.logger.handlers[0])

    @app.before_request
    def request_log():
        app.logger.info(f"request => methods : {request.method}, url : {request.url}")

    @app.after_request
    def response_log(response):
        if not response:
            res = make_response("System error")
            res.status_code = 500
            return res
        app.logger.info(f"response => {response.status}")
        return response
        


    return app







