from flask import request
from flask_jwt_extended import jwt_required,get_jwt_identity
from app.product.models import Product
from extensions import db
from app.product import product_bp


def role_required(role):
    def decorator(fn):
        def wrapper(*args,**kwargs):
            current_user = get_jwt_identity()
            if current_user["UserRole"] == role:
                return fn(*args,**kwargs)
            else:
                return f"Role required : {role}"
        return wrapper
    return decorator


       
@product_bp.route("/product/register",methods=["POST"],endpoint="add_product")
@jwt_required()
@role_required("Admin")
def add_product():
    try:
        product = request.json

        db.session.add(Product(**product))
        db.session.commit()

        return "Product added",201
    except Exception as e:
        return f"Error : {e}",500
    

@product_bp.route("/product/delete/<product>",methods=["DELETE"],endpoint="delete_product")
@jwt_required()
@role_required("Admin")
def add_product(product):
    try:
        product = db.session.execute(db.select(Product).filter_by(ProductId=product)).scalar_one()
        db.session.delete(product)
        db.session.commit()

        return "Product deleted"
    except Exception as e:
        return f"Error : {e}",500


@product_bp.route("/product/get/<product>",methods=["GET"],endpoint="get_product")
@jwt_required()
@role_required("User")
def get_product(product):
    try:
        print("get product")
        product = Product.query.filter_by(ProductName = product).first()
        return f"Product : {product.Name} => {product.price}",200
    except Exception as e:
        return f"Error :{e}",500