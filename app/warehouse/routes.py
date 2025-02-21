from extensions import db
from app.warehouse import warehouse_bp
from app.warehouse.models import Inventory
from flask import request
from flask_jwt_extended import get_jwt_identity,jwt_required

from app.warehouse import warehouse_bp


def role_required(role):
    def decorator(fn):
        def wrapper(*args,**kwargs):
            current_user = get_jwt_identity()
            if current_user["UserRole"] == role:
                return fn(*args,**kwargs)
            else:
                return f"role required : {role}"
        return wrapper
    return decorator

@warehouse_bp.route("/warehouse/register",methods=["POST"],endpoint="register_warehouse")
@jwt_required()
@role_required("Admin")
def register_warehouse():
    try:
        warehouse  = request.json
        db.session.add(Inventory(**warehouse))
        db.session.commit()
        return "added"
    except Exception as e:
        return f"error {e}",500


@warehouse_bp.route("/warehouse/delete/<warehouse>",methods=["DELETE"],endpoint="delete_warehouse")
@jwt_required()
@role_required("Admin")
def delete_invetory(warehouse):
    try:
        warehouse = db.session.execute(db.select(Inventory).filter_by(InventoryId=warehouse)).scalar_one()
        db.session.delete(warehouse)
        db.session.commit()
        return "deleted"
    except Exception as e:
        print(e)
        return f"error {e}",500
