from datetime import datetime
from app.extensions import db

# Association table for project likes
project_likes = db.Table(
    "project_likes",
    db.Column("user_id", db.Integer, db.ForeignKey("users.id"), primary_key=True),
    db.Column("project_id", db.Integer, db.ForeignKey("projects.id"), primary_key=True),
    db.Column("created_at", db.DateTime, default=datetime.utcnow)
)


class Project(db.Model):
    __tablename__ = "projects"

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text, nullable=False)
    stage = db.Column(db.String(50), nullable=False, default="planning")
    support_needed = db.Column(db.Text, nullable=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    owner = db.relationship("User", backref=db.backref("projects", lazy="dynamic", cascade="all, delete-orphan"))
    liked_by = db.relationship(
        "User",
        secondary=project_likes,
        backref=db.backref("liked_projects", lazy="dynamic"),
        lazy="dynamic"
    )

    VALID_STAGES = ["planning", "in_progress", "completed"]

    def __init__(self, title, description, user_id, stage="planning", support_needed=None):
        self.title = title.strip()
        self.description = description.strip()
        self.user_id = user_id
        self.stage = stage if stage in self.VALID_STAGES else "planning"
        self.support_needed = support_needed.strip() if support_needed else None

    def to_dict(self):
        return {
            "id": self.id,
            "title": self.title,
            "description": self.description,
            "stage": self.stage,
            "support_needed": self.support_needed,
            "user_id": self.user_id,
            "owner_username": self.owner.username,
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "updated_at": self.updated_at.isoformat() if self.updated_at else None,
            "likes_count": self.liked_by.count(),
        }

    def is_liked_by(self, user):
        return self.liked_by.filter_by(id=user.id).count() > 0

    def __repr__(self):
        return f"<Project {self.title}>"