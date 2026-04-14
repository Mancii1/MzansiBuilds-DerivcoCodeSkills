from app.extensions import db
from app.models import User, Skill


class ProfileService:
    @staticmethod
    def get_user_profile(user_id):
        """Return user dict or None."""
        user = db.session.get(User, user_id)  # ← UPDATED
        if not user:
            return None
        return user.to_dict()

    @staticmethod
    def update_profile(user_id, data):
        """
        Update user profile fields and skills.
        Returns (user_dict, error_message).
        """
        user = db.session.get(User, user_id)  # ← UPDATED
        if not user:
            return None, "User not found"

        # Update simple fields
        updatable_fields = ["bio", "location", "avatar_url"]
        for field in updatable_fields:
            if field in data:
                setattr(user, field, data[field])

        # Handle skills if provided
        if "skills" in data and isinstance(data["skills"], list):
            skill_objects = []
            for skill_name in data["skills"]:
                if not skill_name or not isinstance(skill_name, str):
                    continue
                skill_name = skill_name.lower().strip()
                if not skill_name:
                    continue
                skill = Skill.query.filter_by(name=skill_name).first()
                if not skill:
                    skill = Skill(name=skill_name)
                    db.session.add(skill)
                skill_objects.append(skill)
            user.skills = skill_objects

        try:
            db.session.commit()
            return user.to_dict(include_email=True), None
        except Exception as e:
            db.session.rollback()
            return None, str(e)