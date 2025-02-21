from flask import request,make_response
from flask_jwt_extended import create_access_token,jwt_required,get_jwt_identity,set_access_cookies,unset_access_cookies
from extensions import db,bcrypt
from app.auth import auth_bp
from app.auth.models import User as Auth
from sqlalchemy.exc import IntegrityError




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


@role_required("Admin")
@auth_bp.route("/auth/signup", methods=["POST"])
def signup():
    try:
        auth = request.json

        auth["UserRole"]=auth.get("UserRole","User")
        auth["Password"]=bcrypt.generate_password_hash(auth["Password"])
        try:
            db.session.add(Auth(**auth))
            db.session.commit()
        except IntegrityError as e:
            return str(e),501

        return f"User '{auth.User}' signup successfull",201
    except Exception as e:
        db.session.rollback()
        return f"Error : {e}",500
    

@auth_bp.route("/auth/sigin", methods=["PUT"])
def signin():
    try:
        data = request.json

        auth = Auth.query.filter_by(UserId = data["UserId"]).first()
        if auth:
            if bcrypt.check_password_hash(auth.Password,data["Password"]):
                res = make_response("signin successfull")

                access_token = create_access_token(identity={"UserId":data["UserId"],"UserRole":auth.UserRole})
                set_access_cookies(res,access_token)
                return res,200
            else:
                return "Already signin", 409
        return "Password mismatch",403

    except Exception as e:
        db.session.rollback()
        return f"Error : {e}",500


@auth_bp.route("/auth/logout",methods=["PUT"])
@jwt_required()
def logout():
    try:
        id = get_jwt_identity()["UserId"]
        auth = Auth.query.filter_by(UserId = id)
        if auth:
            res=make_response("logout success")
            unset_access_cookies(res)
            return res,200
        else:
            return "Login first" ,405
    except Exception as e:
        return f"Error : {e}",500