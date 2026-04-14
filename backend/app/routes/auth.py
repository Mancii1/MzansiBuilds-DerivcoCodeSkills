from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.services.auth_service import AuthService

auth_bp = Blueprint("auth", __name__, url_prefix="/api/auth")


@auth_bp.route("/register", methods=["POST"])
def register():
    """Register a new user."""
    data = request.get_json()
    if not data:
        return jsonify({"error": "No input data provided"}), 400

    email = data.get("email")
    username = data.get("username")
    password = data.get("password")

    # Basic validation
    if not email or not username or not password:
        return jsonify({"error": "Missing required fields: email, username, password"}), 400
    if len(password) < 8:
        return jsonify({"error": "Password must be at least 8 characters long"}), 400

    user, error = AuthService.register_user(email, username, password)
    if error:
        return jsonify({"error": error}), 400

    return jsonify({
        "message": "User registered successfully",
        "user": {
            "id": user.id,
            "email": user.email,
            "username": user.username
        }
    }), 201


@auth_bp.route("/login", methods=["POST"])
def login():
    """Log in and return JWT tokens."""
    data = request.get_json()
    if not data:
        return jsonify({"error": "No input data provided"}), 400

    identifier = data.get("identifier")  # email or username
    password = data.get("password")

    if not identifier or not password:
        return jsonify({"error": "Missing identifier or password"}), 400

    user, access_token, refresh_token, error = AuthService.login_user(identifier, password)
    if error:
        return jsonify({"error": error}), 401

    return jsonify({
        "access_token": access_token,
        "refresh_token": refresh_token,
        "user": {
            "id": user.id,
            "email": user.email,
            "username": user.username
        }
    }), 200


@auth_bp.route("/refresh", methods=["POST"])
@jwt_required(refresh=True)
def refresh():
    """Obtain a new access token using a refresh token."""
    user_id = get_jwt_identity()
    access_token, error = AuthService.refresh_access_token(user_id)
    if error:
        return jsonify({"error": error}), 401
    return jsonify({"access_token": access_token}), 200