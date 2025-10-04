from flask import Blueprint, request, jsonify, current_app
from werkzeug.security import generate_password_hash, check_password_hash
from flask_jwt_extended import jwt_required, get_jwt_identity
from flask_jwt_extended import create_access_token
from datetime import timedelta
from datetime import datetime
import uuid

auth_bp = Blueprint("auth", __name__)

@auth_bp.route("/register", methods=["POST"])
def register():
    data = request.json
    email = data.get("email")
    password = data.get("password")
    if not email or not password:
        return jsonify({"msg":"email & password required"}), 400

    user = current_app.db.users.find_one({"email": email})
    if user:
        return jsonify({"msg":"email already exists"}), 400

    user_doc = {
        "_id": str(uuid.uuid4()),
        "email": email,
        "password": generate_password_hash(password),
        "role": data.get("role","employee"),
        "created_at":  datetime.utcnow()
    }
    current_app.db.users.insert_one(user_doc)
    return jsonify({"msg":"registered"}), 201

@auth_bp.route("/login", methods=["POST"])
def login():
    data = request.json
    email = data.get("email"); password = data.get("password")
    user = current_app.db.users.find_one({"email": email})
    if not user or not check_password_hash(user["password"], password):
        return jsonify({"msg":"invalid credentials"}), 401

    access = create_access_token(identity=user["_id"], expires_delta=timedelta(hours=6))
    return jsonify({"access_token": access, "user_id": user["_id"], "role": user.get("role")})

@auth_bp.route("/assign-role", methods=["POST"])
def assign_role():
    data = request.json
    user_id = data.get("user_id")
    role = data.get("role")
    if not user_id or not role:
        return jsonify({"msg": "user_id and role required"}), 400

    result = current_app.db.users.update_one({"_id": user_id}, {"$set": {"role": role}})
    if result.modified_count == 0:
        return jsonify({"msg":"user not found"}), 404

    return jsonify({"msg":"role updated"}), 200



# ---------------- Admin Create User ----------------
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

import random
import string

def generate_random_password(length=8):
    chars = string.ascii_letters + string.digits + "!@#$%^&*()"
    return ''.join(random.choice(chars) for _ in range(length))

def send_password_email(to_email, name, password):
    sender_email = "your_email@gmail.com"       # replace with your email
    sender_password = "your_app_password"       # use app password (Gmail)

    message = MIMEMultipart()
    message["From"] = sender_email
    message["To"] = to_email
    message["Subject"] = "Your Account Password"

    body = f"""
    Hi {name},

    Your account has been created successfully.

    Login Credentials:
    Email: {to_email}
    Password: {password}

    Please change your password after first login.
    """
    message.attach(MIMEText(body, "plain"))

    try:
        with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
            server.login(sender_email, sender_password)
            server.sendmail(sender_email, to_email, message.as_string())
        print(f"Email sent successfully to {to_email}")
    except Exception as e:
        print(f"Failed to send email: {e}")
        raise e


@auth_bp.route("/admin/create-user", methods=["POST"])
@jwt_required(optional=True)
def admin_create_user():
    admin_id = get_jwt_identity()
    admin = current_app.db.users.find_one({"_id": admin_id})
    if not admin or admin.get("role") != "admin":
        return jsonify({"msg": "Unauthorized"}), 403

    data = request.json
    email = data.get("email")
    role = data.get("role", "employee")
    name = data.get("name", "")

    if not email or not name:
        return jsonify({"msg":"Name and email are required"}), 400

    if current_app.db.users.find_one({"email": email}):
        return jsonify({"msg":"Email already exists"}), 400

    # Generate random password
    password = generate_random_password()

    user_doc = {
        "_id": str(uuid.uuid4()),
        "name": name,
        "email": email,
        "password": generate_password_hash(password),
        "role": role,
        "created_at": datetime.utcnow()
    }
    current_app.db.users.insert_one(user_doc)

    # Send password via email
    try:
        send_password_email(email, name, password)
    except Exception as e:
        print(f"Email sending failed: {e}")

    return jsonify({"msg":"User created, password sent via email", "user_id": user_doc["_id"]}), 201
