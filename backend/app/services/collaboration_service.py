from app.extensions import db
from app.models import CollaborationRequest, Project, User


class CollaborationService:
    @staticmethod
    def create_request(requester_id, project_id, message=None):
        """Create a new collaboration request."""
        project = db.session.get(Project, project_id)
        if not project:
            return None, "Project not found"

        if project.user_id == requester_id:
            return None, "You cannot request collaboration on your own project"

        existing = CollaborationRequest.query.filter_by(
            project_id=project_id, requester_id=requester_id, status="pending"
        ).first()
        if existing:
            return None, "You already have a pending request for this project"

        request = CollaborationRequest(
            project_id=project_id,
            requester_id=requester_id,
            message=message
        )
        db.session.add(request)
        db.session.commit()
        return request, None

    @staticmethod
    def update_request_status(request_id, owner_id, new_status):
        """Accept or reject a request (owner only)."""
        req = db.session.get(CollaborationRequest, request_id)
        if not req:
            return None, "Request not found"

        if req.project.user_id != owner_id:
            return None, "You do not have permission to manage this request"

        if new_status not in CollaborationRequest.VALID_STATUSES:
            return None, f"Invalid status. Must be one of: {', '.join(CollaborationRequest.VALID_STATUSES)}"

        if req.status != "pending":
            return None, f"Request is already {req.status}"

        req.status = new_status
        db.session.commit()
        return req, None

    @staticmethod
    def get_incoming_requests(owner_id, status=None):
        query = CollaborationRequest.query.join(Project).filter(Project.user_id == owner_id)
        if status:
            query = query.filter(CollaborationRequest.status == status)
        requests = query.order_by(CollaborationRequest.created_at.desc()).all()
        return [r.to_dict() for r in requests], None

    @staticmethod
    def get_outgoing_requests(requester_id, status=None):
        query = CollaborationRequest.query.filter_by(requester_id=requester_id)
        if status:
            query = query.filter_by(status=status)
        requests = query.order_by(CollaborationRequest.created_at.desc()).all()
        return [r.to_dict() for r in requests], None