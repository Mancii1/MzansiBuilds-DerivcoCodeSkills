from datetime import datetime
from app.extensions import db


class Milestone(db.Model):
    __tablename__ = "milestones"

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text, nullable=True)
    due_date = db.Column(db.Date, nullable=True)
    completed = db.Column(db.Boolean, default=False, nullable=False)
    project_id = db.Column(db.Integer, db.ForeignKey("projects.id"), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationship
    project = db.relationship("Project", backref=db.backref("milestones", lazy="dynamic", cascade="all, delete-orphan"))

    def __init__(self, title, project_id, description=None, due_date=None):
        self.title = title.strip()
        self.project_id = project_id
        self.description = description.strip() if description else None
        self.due_date = due_date
        self.completed = False

    def to_dict(self):
        return {
            "id": self.id,
            "title": self.title,
            "description": self.description,
            "due_date": self.due_date.isoformat() if self.due_date else None,
            "completed": self.completed,
            "project_id": self.project_id,
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "updated_at": self.updated_at.isoformat() if self.updated_at else None,
        }

    def __repr__(self):
        return f"<Milestone {self.title} - {'✓' if self.completed else '○'}>"