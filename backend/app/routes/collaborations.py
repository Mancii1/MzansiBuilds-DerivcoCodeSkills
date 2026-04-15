from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.services.collaboration_service import CollaborationService

collaborations_bp = Blueprint("collaborations", __name__, url_prefix="/api")


@collaborations_bp.route("/projects/<int:project_id>/collaborate", methods=["POST"])
@jwt_required()
def request_collaboration(project_id):
    """Send a collaboration request for a project."""
    user_id = int(get_jwt_identity())
    data = request.get_json() or {}
    message = data.get("message")

    req, error = CollaborationService.create_request(user_id, project_id, message)
    if error:
        status_code = 400 if "already" in error or "own project" in error else 404
        return jsonify({"error": error}), status_code

    return jsonify(req.to_dict()), 201


@collaborations_bp.route("/collaborations/incoming", methods=["GET"])
@jwt_required()
def get_incoming_requests():
    """Get collaboration requests for projects owned by current user."""
    user_id = int(get_jwt_identity())
    status = request.args.get("status")
    requests, error = CollaborationService.get_incoming_requests(user_id, status)
    return jsonify(requests), 200


@collaborations_bp.route("/collaborations/outgoing", methods=["GET"])
@jwt_required()
def get_outgoing_requests():
    """Get collaboration requests sent by current user."""
    user_id = int(get_jwt_identity())
    status = request.args.get("status")
    requests, error = CollaborationService.get_outgoing_requests(user_id, status)
    return jsonify(requests), 200


@collaborations_bp.route("/collaborations/<int:request_id>/accept", methods=["PATCH"])
@jwt_required()
def accept_request(request_id):
    """Accept a collaboration request (owner only)."""
    user_id = int(get_jwt_identity())
    req, error = CollaborationService.update_request_status(request_id, user_id, "accepted")
    if error:
        status_code = 403 if "permission" in error.lower() else 400 if "already" in error.lower() else 404
        return jsonify({"error": error}), status_code
    return jsonify(req.to_dict()), 200


@collaborations_bp.route("/collaborations/<int:request_id>/reject", methods=["PATCH"])
@jwt_required()
def reject_request(request_id):
    """Reject a collaboration request (owner only)."""
    user_id = int(get_jwt_identity())
    req, error = CollaborationService.update_request_status(request_id, user_id, "rejected")
    if error:
        status_code = 403 if "permission" in error.lower() else 400 if "already" in error.lower() else 404
        return jsonify({"error": error}), status_code
    return jsonify(req.to_dict()), 200