from flask import Blueprint, request, jsonify, current_app
from flask_jwt_extended import jwt_required, get_jwt_identity
from datetime import datetime
import uuid

expense_bp = Blueprint("expenses", __name__)

# ---------------- Create Expense ----------------
@expense_bp.route("/", methods=["POST"])
@jwt_required()
def create_expense():
    user_id = get_jwt_identity()

    # Handle form-data with file upload or JSON
    if request.content_type and request.content_type.startswith("multipart/form-data"):
        form = request.form
        file = request.files.get("receipt")
    else:
        form = request.json
        file = None

    # Validate required fields
    if not form.get("title") or not form.get("amount"):
        return jsonify({"msg": "title and amount are required"}), 400

    doc = {
        "_id": str(uuid.uuid4()),
        "user_id": user_id,
        "title": form.get("title"),
        "amount": float(form.get("amount", 0)),
        "currency": form.get("currency", "INR"),
        "category": form.get("category", "other"),
        "notes": form.get("notes"),
        "status": "pending",
        "created_at": datetime.utcnow(),
        "updated_at": datetime.utcnow()
    }

    # Optional: Save receipt file in GridFS
    if file:
        fs_id = current_app.fs.put(file.read(), filename=file.filename, contentType=file.mimetype)
        doc["receipt_file_id"] = fs_id

    current_app.db.expenses.insert_one(doc)
    return jsonify({"expense_id": doc["_id"]}), 201

# ---------------- Get Expense ----------------
@expense_bp.route("/<expense_id>", methods=["GET"])
@jwt_required()
def get_expense(expense_id):
    user_id = get_jwt_identity()
    expense = current_app.db.expenses.find_one({"_id": expense_id})

    if not expense:
        return jsonify({"msg": "Expense not found"}), 404

    # Optional: Authorization check
    # Employees can only see their own expenses, managers/admins can see all
    if expense["user_id"] != user_id:
        # Here you can add role-based logic using current_app.db.users
        return jsonify({"msg": "Unauthorized"}), 403

    # Convert MongoDB ObjectId to string if necessary
    if "_id" in expense:
        expense["_id"] = str(expense["_id"])
    if "receipt_file_id" in expense:
        expense["receipt_file_id"] = str(expense["receipt_file_id"])

    return jsonify(expense)
