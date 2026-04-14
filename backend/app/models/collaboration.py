from datetime import datetime
from app.extensions import db


class CollaborationRequest(db.Model):
    __tablename__ = "collaboration_requests"

    id = db.Column(db.Integer, primary_key=True)
    project_id = db.Column(db.Integer, db.ForeignKey("projects.id"), nullable=False)
    requester_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    status = db.Column(db.String(20), nullable=False, default="pending")  # pending, accepted, rejected
    message = db.Column(db.Text, nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationships
    project = db.relationship("Project", backref=db.backref("collaboration_requests", lazy="dynamic", cascade="all, delete-orphan"))
    requester = db.relationship("User", backref=db.backref("sent_requests", lazy="dynamic", cascade="all, delete-orphan"))

    VALID_STATUSES = ["pending", "accepted", "rejected"]

    def __init__(self, project_id, requester_id, message=None):
        self.project_id = project_id
        self.requester_id = requester_id
        self.message = message.strip() if message else None
        self.status = "pending"

    def to_dict(self):
        return {
            "id": self.id,
            "project_id": self.project_id,
            "project_title": self.project.title,
            "requester_id": self.requester_id,
            "requester_username": self.requester.username,
            "status": self.status,
            "message": self.message,
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "updated_at": self.updated_at.isoformat() if self.updated_at else None,
        }

    def __repr__(self):
        return f"<CollaborationRequest {self.id} - {self.status}>"