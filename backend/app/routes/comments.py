from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.services.comment_service import CommentService

comments_bp = Blueprint("comments", __name__, url_prefix="/api/projects")


@comments_bp.route("/<int:project_id>/comments", methods=["POST"])
@jwt_required()
def add_comment(project_id):
    """Add a comment to a project."""
    user_id = int(get_jwt_identity())
    data = request.get_json()
    if not data or "content" not in data:
        return jsonify({"error": "Missing comment content"}), 400

    comment, error = CommentService.add_comment(user_id, project_id, data["content"])
    if error:
        status_code = 404 if "not found" in error.lower() else 400
        return jsonify({"error": error}), status_code

    return jsonify(comment.to_dict()), 201


@comments_bp.route("/<int:project_id>/comments", methods=["GET"])
def get_comments(project_id):
    """Get all comments for a project."""
    comments, error = CommentService.get_comments_for_project(project_id)
    if error:
        return jsonify({"error": error}), 404
    return jsonify(comments), 200


@comments_bp.route("/comments/<int:comment_id>", methods=["DELETE"])
@jwt_required()
def delete_comment(comment_id):
    """Delete a comment (owner only)."""
    user_id = int(get_jwt_identity())
    success, error = CommentService.delete_comment(comment_id, user_id)
    if error:
        status_code = 403 if "permission" in error.lower() else 404
        return jsonify({"error": error}), status_code
    return jsonify({"message": "Comment deleted successfully"}), 200