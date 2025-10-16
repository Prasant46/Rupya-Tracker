from flask import Blueprint, request, jsonify
from app.extensions import db
from app.models.user import User
from flask_jwt_extended import jwt_required, get_jwt_identity

bp = Blueprint("users", __name__, url_prefix="/users")

@bp.route("/", methods=["POST"])
def create_user():
  data = request.get_json() or {}
  if not data:
    return jsonify({
      "success": False,
      "message": "Data should not be empty"
    }), 400
  
  account_id = data.get("accountId")
  name = data.get("name")
  email = data.get("email")
  avatar = data.get("avatarUrl")
  
  if not (account_id and name and email):
    return jsonify({
      "success": False,
      "message": "Enter valid details"
    }), 400
  
  if User.query.filter_by(account_id=account_id).first() or User.query.filter_by(email=email).first() :
    return jsonify({
      "success": False,
      "message": "User with this account ID or email already exists"
    }), 400
  
  user = User(account_id=account_id, name=name, email=email, avatar=avatar)
  db.session.add(user)
  db.session.commit()
  
  return jsonify({
    "success": True,
    "message": "User created successfully",
    "data": user.to_dict()
  }), 201
  
@bp.route("/me", methods=["GET"])
@jwt_required(optional=True)
def get_current_user():
  identity = get_jwt_identity()
  
  if not identity:
    return jsonify({
      "success": True,
      "message": "No user logged in",
      "data": None
    }), 200
  
  user = User.query.filter_by(account_id=identity).first()
  
  if not user:
    return jsonify({
      "success": True,
      "message": "User not found",
      "data": None
    }), 200
  
  return jsonify({
    "success": True,
    "data": user.to_dict()
  }), 200