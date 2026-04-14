from flask import Blueprint, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.services.like_service import LikeService

likes_bp = Blueprint("likes", __name__, url_prefix="/api/projects")


@likes_bp.route("/<int:project_id>/like", methods=["POST"])
@jwt_required()
def toggle_like(project_id):
    """Like or unlike a project."""
    user_id = int(get_jwt_identity())
    liked, error = LikeService.toggle_like(user_id, project_id)
    if error:
        return jsonify({"error": error}), 404
    return jsonify({"liked": liked}), 200


@likes_bp.route("/<int:project_id>/likes", methods=["GET"])
def get_likes(project_id):
    """Get list of users who liked the project and total count."""
    likers, error = LikeService.get_likers(project_id)
    if error:
        return jsonify({"error": error}), 404
    return jsonify({"count": len(likers), "likers": likers}), 200