from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.services.project_service import ProjectService

projects_bp = Blueprint("projects", __name__, url_prefix="/api/projects")


@projects_bp.route("", methods=["POST"])
@jwt_required()
def create_project():
    """Create a new project."""
    user_id = int(get_jwt_identity())
    data = request.get_json()
    if not data:
        return jsonify({"error": "No input data provided"}), 400

    project, error = ProjectService.create_project(user_id, data)
    if error:
        return jsonify({"error": error}), 400

    return jsonify(project.to_dict()), 201


@projects_bp.route("/<int:project_id>", methods=["GET"])
def get_project(project_id):
    """Get a single project."""
    project, error = ProjectService.get_project(project_id)
    if error:
        return jsonify({"error": error}), 404
    return jsonify(project.to_dict()), 200


@projects_bp.route("/<int:project_id>", methods=["PUT"])
@jwt_required()
def update_project(project_id):
    """Update a project (owner only)."""
    user_id = int(get_jwt_identity())
    data = request.get_json()
    if not data:
        return jsonify({"error": "No input data provided"}), 400

    project, error = ProjectService.update_project(project_id, user_id, data)
    if error:
        status_code = 403 if "permission" in error.lower() else 400 if "invalid stage" in error.lower() else 404
        return jsonify({"error": error}), status_code

    return jsonify(project.to_dict()), 200


@projects_bp.route("/<int:project_id>", methods=["DELETE"])
@jwt_required()
def delete_project(project_id):
    """Delete a project (owner only)."""
    user_id = int(get_jwt_identity())
    success, error = ProjectService.delete_project(project_id, user_id)
    if error:
        status_code = 403 if "permission" in error.lower() else 404
        return jsonify({"error": error}), status_code
    return jsonify({"message": "Project deleted successfully"}), 200


@projects_bp.route("/feed", methods=["GET"])
def get_feed():
    """Get paginated project feed with sorting."""
    sort_by = request.args.get("sort", "latest")
    page = request.args.get("page", 1, type=int)
    per_page = request.args.get("per_page", 20, type=int)

    result, error = ProjectService.get_feed(sort_by=sort_by, page=page, per_page=per_page)
    if error:
        return jsonify({"error": error}), 400
    return jsonify(result), 200


@projects_bp.route("/celebration-wall", methods=["GET"])
def celebration_wall():
    """Get paginated list of completed projects (Celebration Wall)."""
    sort_by = request.args.get("sort", "latest")
    page = request.args.get("page", 1, type=int)
    per_page = request.args.get("per_page", 20, type=int)

    result, error = ProjectService.get_completed_projects(sort_by=sort_by, page=page, per_page=per_page)
    if error:
        return jsonify({"error": error}), 400
    return jsonify(result), 200