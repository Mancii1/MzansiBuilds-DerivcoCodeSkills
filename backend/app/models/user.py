from datetime import datetime
from app.extensions import db, bcrypt

# Association table for User <-> Skill many-to-many
user_skills = db.Table(
    "user_skills",
    db.Column("user_id", db.Integer, db.ForeignKey("users.id"), primary_key=True),
    db.Column("skill_id", db.Integer, db.ForeignKey("skills.id"), primary_key=True),
)


class User(db.Model):
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False, index=True)
    username = db.Column(db.String(80), unique=True, nullable=False, index=True)
    password_hash = db.Column(db.String(128), nullable=False)
    
    # Profile fields
    bio = db.Column(db.Text, nullable=True)
    location = db.Column(db.String(100), nullable=True)
    avatar_url = db.Column(db.String(255), nullable=True)
    
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationships
    skills = db.relationship("Skill", secondary=user_skills, backref=db.backref("users", lazy="dynamic"))

    def __init__(self, email, username, password):
        self.email = email.lower().strip()
        self.username = username.strip()
        self.password_hash = bcrypt.generate_password_hash(password).decode("utf-8")

    def check_password(self, password):
        return bcrypt.check_password_hash(self.password_hash, password)

    def to_dict(self, include_email=False):
        """Serialise user to dict, optionally including email."""
        data = {
            "id": self.id,
            "username": self.username,
            "bio": self.bio,
            "location": self.location,
            "avatar_url": self.avatar_url,
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "skills": [skill.name for skill in self.skills],
        }
        if include_email:
            data["email"] = self.email
        return data

    def __repr__(self):
        return f"<User {self.username}>"