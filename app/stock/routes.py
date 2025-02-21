from flask import request
from flask_jwt_extended import get_jwt_identity,jwt_required
from app.warehouse.models import Inventory
from app.product.models import Product
from app.stock.models import Stock
from app.stock import stock_bp
from extensions import db

def role_required(role):
    def decorator(fn):
        # @wraps(fn)
        def wrapper(*args,**kwargs):
            current_user = get_jwt_identity()
            if current_user["UserRole"] == role:
                return fn(*args,**kwargs)
            else:
                return f"role required : {role}"
        return wrapper
    return decorator

@stock_bp.route("/inventory/add_stock",methods = ["POST"],endpoint="register_stock")
@jwt_required()
@role_required("Admin")
def add_stock():
    try:
        stock = request.json
        product = db.session.execute(db.select(Product).filter_by(ProductId=stock["ProductId"])).scalar_one()
        if product:
            inventory = db.session.execute(db.select(Inventory).filter_by(InventoryId=stock["InventoryId"])).scalar_one()
            if inventory:
                print(stock)
                db.session.add(Stock(**stock))
                db.session.commit()
                return "added"
            else:
                return "No inventory"
        else:
            return 'No product'
    except Exception as e:
        print("error")
        return f"{e}",500
    

@stock_bp.route("/inventory/del_stock/<stock>",methods = ["POST"],endpoint="delete_stock")
@jwt_required()
@role_required("Admin")
def delete_stock(stock):
    try:
        stock = db.session.execute(db.select(Stock).filter_by(Id=stock)).scalar_one()
        if stock:
            db.session.delete(stock)
            db.session.commit()
            return "delete success"

        else:
            return 'No product'
    except Exception as e:
        return f"{e}",500
    

@stock_bp.route("/stock/<stock>",methods=["GET"])
@jwt_required()
@role_required("Admin")
def get_stock(stock):
    try:
        a=db.session.query(Stock,Product).join(Product,Stock.ProductId==Product.ProductId).all()
        d={}
        for i in a:
            print(i[0],i[1])
            d[i[0].Id]=str(i[0])+str(i[1])
        return d
    except Exception as e:
        return f"{e}",500