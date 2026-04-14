from datetime import datetime
from app.extensions import db


class Comment(db.Model):
    __tablename__ = "comments"

    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.Text, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    project_id = db.Column(db.Integer, db.ForeignKey("projects.id"), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    author = db.relationship("User", backref=db.backref("comments", lazy="dynamic", cascade="all, delete-orphan"))
    project = db.relationship("Project", backref=db.backref("comments", lazy="dynamic", cascade="all, delete-orphan"))

    def __init__(self, content, user_id, project_id):
        self.content = content.strip()
        self.user_id = user_id
        self.project_id = project_id

    def to_dict(self):
        return {
            "id": self.id,
            "content": self.content,
            "user_id": self.user_id,
            "author_username": self.author.username,
            "project_id": self.project_id,
            "created_at": self.created_at.isoformat() if self.created_at else None,
        }

    def __repr__(self):
        return f"<Comment {self.id} by {self.author.username}>"