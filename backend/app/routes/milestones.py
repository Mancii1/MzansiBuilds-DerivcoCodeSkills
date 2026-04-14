from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.services.milestone_service import MilestoneService

milestones_bp = Blueprint("milestones", __name__, url_prefix="/api/projects")


@milestones_bp.route("/<int:project_id>/milestones", methods=["POST"])
@jwt_required()
def create_milestone(project_id):
    """Create a new milestone for a project."""
    user_id = int(get_jwt_identity())
    data = request.get_json()
    if not data:
        return jsonify({"error": "No input data provided"}), 400

    milestone, error = MilestoneService.create_milestone(project_id, user_id, data)
    if error:
        status_code = 403 if "permission" in error.lower() else 400 if "required" in error.lower() or "format" in error.lower() else 404
        return jsonify({"error": error}), status_code

    return jsonify(milestone.to_dict()), 201


@milestones_bp.route("/<int:project_id>/milestones", methods=["GET"])
def get_milestones(project_id):
    """Get all milestones for a project."""
    milestones, error = MilestoneService.get_milestones_for_project(project_id)
    if error:
        return jsonify({"error": error}), 404
    return jsonify(milestones), 200


@milestones_bp.route("/<int:project_id>/progress", methods=["GET"])
def get_progress(project_id):
    """Get milestone progress for a project."""
    progress, error = MilestoneService.get_progress(project_id)
    if error:
        return jsonify({"error": error}), 404
    return jsonify(progress), 200


@milestones_bp.route("/milestones/<int:milestone_id>", methods=["PUT"])
@jwt_required()
def update_milestone(milestone_id):
    """Update milestone details."""
    user_id = int(get_jwt_identity())
    data = request.get_json()
    if not data:
        return jsonify({"error": "No input data provided"}), 400

    milestone, error = MilestoneService.update_milestone(milestone_id, user_id, data)
    if error:
        status_code = 403 if "permission" in error.lower() else 400 if "format" in error.lower() else 404
        return jsonify({"error": error}), status_code

    return jsonify(milestone.to_dict()), 200


@milestones_bp.route("/milestones/<int:milestone_id>", methods=["DELETE"])
@jwt_required()
def delete_milestone(milestone_id):
    """Delete a milestone."""
    user_id = int(get_jwt_identity())
    success, error = MilestoneService.delete_milestone(milestone_id, user_id)
    if error:
        status_code = 403 if "permission" in error.lower() else 404
        return jsonify({"error": error}), status_code
    return jsonify({"message": "Milestone deleted successfully"}), 200


@milestones_bp.route("/milestones/<int:milestone_id>/toggle", methods=["PATCH"])
@jwt_required()
def toggle_complete(milestone_id):
    """Toggle milestone completion status."""
    user_id = int(get_jwt_identity())
    milestone, error = MilestoneService.toggle_complete(milestone_id, user_id)
    if error:
        status_code = 403 if "permission" in error.lower() else 404
        return jsonify({"error": error}), status_code
    return jsonify(milestone.to_dict()), 200