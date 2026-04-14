from app.extensions import db
from app.models import Project, User


class LikeService:
    @staticmethod
    def toggle_like(user_id, project_id):
        user = db.session.get(User, user_id)
        if not user:
            return None, "User not found"

        project = db.session.get(Project, project_id)
        if not project:
            return None, "Project not found"

        if project.is_liked_by(user):
            project.liked_by.remove(user)
            liked = False
        else:
            project.liked_by.append(user)
            liked = True

        try:
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            return None, str(e)

        return liked, None

    @staticmethod
    def get_likers(project_id):
        project = db.session.get(Project, project_id)
        if not project:
            return None, "Project not found"
        likers = [user.username for user in project.liked_by]
        return likers, None