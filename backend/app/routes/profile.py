from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.services.profile_service import ProfileService

profile_bp = Blueprint("profile", __name__, url_prefix="/api")


@profile_bp.route("/profile", methods=["GET"])
@jwt_required()
def get_own_profile():
    """Return the authenticated user's profile."""
    user_id = int(get_jwt_identity())
    profile = ProfileService.get_user_profile(user_id)
    if not profile:
        return jsonify({"error": "User not found"}), 404
    # Include email for own profile
    from app.models import User
    user = User.query.get(user_id)
    return jsonify(user.to_dict(include_email=True)), 200


@profile_bp.route("/profile", methods=["PUT"])
@jwt_required()
def update_own_profile():
    """Update the authenticated user's profile."""
    user_id = int(get_jwt_identity())
    data = request.get_json()
    if not data:
        return jsonify({"error": "No input data provided"}), 400

    # Optional validation
    allowed_fields = {"bio", "location", "avatar_url", "skills"}
    invalid_fields = set(data.keys()) - allowed_fields
    if invalid_fields:
        return jsonify({"error": f"Invalid fields: {', '.join(invalid_fields)}"}), 400

    updated_profile, error = ProfileService.update_profile(user_id, data)
    if error:
        return jsonify({"error": error}), 400

    return jsonify(updated_profile), 200


@profile_bp.route("/users/<int:user_id>", methods=["GET"])
def get_public_profile(user_id):
    """Return public profile of a user."""
    profile = ProfileService.get_user_profile(user_id)
    if not profile:
        return jsonify({"error": "User not found"}), 404
    # Remove email for public view (already omitted in to_dict without flag)
    return jsonify(profile), 200