from flask import Blueprint, request, jsonify
from app.extensions import db
from app.models.user import User
from app.models.expenses import Expense
from flask_jwt_extended import jwt_required, get_jwt_identity
from datetime import datetime, date
from sqlalchemy import and_

bp = Blueprint("expenses", __name__, url_prefix="/expenses")

@bp.route("", methods=["GET"])
@jwt_required(optional=True)
def list_expenses():
    user_id = request.args.get("userId")
    for_today = request.args.get("forToday", "false").lower() in ("true", "1", "yes")
    
    # Always filter out trashed expenses in main list
    query = Expense.query.filter(Expense.is_trashed == False)

    if user_id:
        query = query.filter(Expense.user_id == user_id)
    if for_today:
        today = date.today()
        start = datetime.combine(today, datetime.min.time())
        end = datetime.combine(today, datetime.max.time())
        query = query.filter(Expense.date.between(start, end))

    results = [e.to_dict() for e in query.order_by(Expense.date.desc()).all()]
    
    return jsonify({
        "success": True,
        "message": "Expenses fetched successfully",
        "data": results
    }), 200


@bp.route("", methods=["POST"])
@jwt_required()
def create_or_update_expense():
   
    data = request.get_json() or {}
    if not data:
        return jsonify({
            "success": False,
            "message": "Data should not be empty"
        }), 400
    
    expense_id = data.get("$id") or data.get("id")
    user_id = data.get("owner")
    title = data.get("title")
    amount = data.get("amount")
    date_s = data.get("date")
    description = data.get("description", "")
    expense_type = data.get("expenseType", "Public")
    
    # Update existing expense
    if expense_id:
        exp = Expense.query.get(expense_id)
        if not exp:
            return jsonify({
                "success": False,
                "message": "Expense not found"
            }), 404
        
        # Update fields if provided
        if title:
            exp.title = title
        if amount is not None:
            exp.amount = amount
        if date_s:
            try:
                dt = datetime.fromisoformat(date_s.replace('Z', '+00:00'))
                exp.date = dt
            except (ValueError, AttributeError):
                return jsonify({
                    "success": False,
                    "message": "Invalid date format"
                }), 400
        if description is not None:
            exp.description = description
        if expense_type:
            exp.expense_type = expense_type
        
        db.session.commit()
        
        return jsonify({
            "success": True,
            "message": "Expense updated successfully",
            "data": exp.to_dict()
        }), 200
    
    # Create new expense
    if not (user_id and title and amount and date_s):
        return jsonify({
            "success": False,
            "message": "owner, title, amount, and date are required"
        }), 400
    
    try:
        dt = datetime.fromisoformat(date_s.replace('Z', '+00:00'))
    except (ValueError, AttributeError):
        return jsonify({
            "success": False,
            "message": "Invalid date format. Use ISO format."
        }), 400
    
    exp = Expense(
        user_id=user_id,
        title=title,
        amount=amount,
        date=dt,
        is_trashed=False,
        description=description,
        expense_type=expense_type
    )
    db.session.add(exp)
    db.session.commit()
    
    return jsonify({
        "success": True,
        "message": "Expense created successfully",
        "data": exp.to_dict()
    }), 201


@bp.route("/<expense_id>", methods=["PUT"])
@jwt_required()
def update_expense_by_id(expense_id):
    """Alternative update endpoint for PUT /expenses/:id"""
    data = request.get_json() or {}
    if not data:
        return jsonify({
            "success": False,
            "message": "Data should not be empty"
        }), 400
    
    exp = Expense.query.get(expense_id)
    if not exp:
        return jsonify({
            "success": False,
            "message": "Expense not found"
        }), 404
    
    # Update fields if provided
    if "title" in data:
        exp.title = data["title"]
    if "amount" in data:
        exp.amount = data["amount"]
    if "date" in data:
        try:
            dt = datetime.fromisoformat(data["date"].replace('Z', '+00:00'))
            exp.date = dt
        except (ValueError, AttributeError):
            return jsonify({
                "success": False,
                "message": "Invalid date format"
            }), 400
    if "description" in data:
        exp.description = data["description"]
    if "expenseType" in data:
        exp.expense_type = data["expenseType"]
    
    db.session.commit()
    
    return jsonify({
        "success": True,
        "message": "Expense updated successfully",
        "data": exp.to_dict()
    }), 200


@bp.route("/<expense_id>", methods=["DELETE"])
@jwt_required()
def delete_expense(expense_id):
    exp = Expense.query.get(expense_id)
    if not exp:
        return jsonify({
            "success": False,
            "message": "Expense not found"
        }), 404
    
    db.session.delete(exp)
    db.session.commit()
    
    return jsonify({
        "success": True,
        "message": "Expense deleted successfully",
        "data": None
    }), 200
  
@bp.route("/trashed", methods=["GET"])
@jwt_required(optional=True)
def get_trashed_expenses():
    # Accept both 'owner' and 'userId' query params
    user_id = request.args.get("owner") or request.args.get("userId")
    if not user_id:
        return jsonify({
            "success": False,
            "message": "owner or userId query parameter is required"
        }), 400
    
    expenses = Expense.query.filter(
        and_(Expense.user_id == user_id, Expense.is_trashed == True)
    ).order_by(Expense.date.desc()).all()
    
    return jsonify({
        "success": True,
        "message": "Trashed expenses fetched successfully",
        "data": [e.to_dict() for e in expenses]
    }), 200

  
@bp.route("/<expense_id>/trash", methods=["POST"])
@jwt_required()
def move_to_trash(expense_id):
    data = request.get_json() or {}
    user_id = data.get("owner") or data.get("user_id")
    
    exp = Expense.query.get(expense_id)
    if not exp:
        return jsonify({
            "success": False,
            "message": "Expense not found"
        }), 404
    
    # Verify ownership if user_id provided
    if user_id and exp.user_id != user_id:
        return jsonify({
            "success": False,
            "message": "Unauthorized"
        }), 403
    
    exp.is_trashed = True
    db.session.commit()
    
    return jsonify({
        "success": True,
        "message": "Expense moved to trash successfully",
        "data": exp.to_dict()
    }), 200

  
@bp.route("/<expense_id>/restore", methods=["POST"])
@jwt_required()
def restore_expense(expense_id):
    data = request.get_json() or {}
    # Accept both 'owner' and 'user_id'
    user_id = data.get("owner") or data.get("user_id")
    
    exp = Expense.query.get(expense_id)
    if not exp:
        return jsonify({
            "success": False,
            "message": "Expense not found"
        }), 404
    
    if user_id and exp.user_id != user_id:
        return jsonify({
            "success": False,
            "message": "Unauthorized"
        }), 403
    
    exp.is_trashed = False
    db.session.commit()
    
    return jsonify({
        "success": True,
        "message": "Expense restored successfully",
        "data": exp.to_dict()
    }), 200  
  
  
  