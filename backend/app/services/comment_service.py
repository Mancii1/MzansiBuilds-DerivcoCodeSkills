from app.extensions import db
from app.models import Comment, Project


class CommentService:
    @staticmethod
    def add_comment(user_id, project_id, content):
        project = db.session.get(Project, project_id)
        if not project:
            return None, "Project not found"

        comment = Comment(content=content, user_id=user_id, project_id=project_id)
        db.session.add(comment)
        db.session.commit()
        return comment, None

    @staticmethod
    def get_comments_for_project(project_id):
        project = db.session.get(Project, project_id)
        if not project:
            return None, "Project not found"

        comments = Comment.query.filter_by(project_id=project_id).order_by(Comment.created_at.desc()).all()
        return [c.to_dict() for c in comments], None

    @staticmethod
    def delete_comment(comment_id, user_id):
        comment = db.session.get(Comment, comment_id)
        if not comment:
            return None, "Comment not found"
        if comment.user_id != user_id:
            return None, "You do not have permission to delete this comment"

        db.session.delete(comment)
        db.session.commit()
        return True, None