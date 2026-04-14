from sqlalchemy import func
from app.extensions import db
from app.models.project import Project, project_likes


class ProjectService:
    @staticmethod
    def create_project(user_id, data):
        required_fields = ["title", "description"]
        for field in required_fields:
            if field not in data:
                return None, f"Missing required field: {field}"

        project = Project(
            title=data["title"],
            description=data["description"],
            user_id=user_id,
            stage=data.get("stage", "planning"),
            support_needed=data.get("support_needed")
        )
        db.session.add(project)
        db.session.commit()
        return project, None

    @staticmethod
    def get_project(project_id):
        project = db.session.get(Project, project_id)
        if not project:
            return None, "Project not found"
        return project, None

    @staticmethod
    def update_project(project_id, user_id, data):
        project = db.session.get(Project, project_id)
        if not project:
            return None, "Project not found"
        if project.user_id != user_id:
            return None, "You do not have permission to update this project"

        updatable_fields = ["title", "description", "stage", "support_needed"]
        for field in updatable_fields:
            if field in data:
                if field == "stage" and data[field] not in Project.VALID_STAGES:
                    return None, f"Invalid stage. Must be one of: {', '.join(Project.VALID_STAGES)}"
                setattr(project, field, data[field])

        db.session.commit()
        return project, None

    @staticmethod
    def delete_project(project_id, user_id):
        project = db.session.get(Project, project_id)
        if not project:
            return None, "Project not found"
        if project.user_id != user_id:
            return None, "You do not have permission to delete this project"

        db.session.delete(project)
        db.session.commit()
        return True, None

    @staticmethod
    def get_feed(sort_by="latest", page=1, per_page=20):
        query = Project.query

        if sort_by == "oldest":
            query = query.order_by(Project.created_at.asc())
        elif sort_by == "most_liked":
            query = query.outerjoin(project_likes).group_by(Project.id).order_by(
                func.count(project_likes.c.user_id).desc(), Project.created_at.desc()
            )
        else:
            query = query.order_by(Project.created_at.desc())

        pagination = query.paginate(page=page, per_page=per_page, error_out=False)
        return {
            "items": [p.to_dict() for p in pagination.items],
            "total": pagination.total,
            "page": pagination.page,
            "pages": pagination.pages,
            "per_page": pagination.per_page,
        }, None

    @staticmethod
    def get_completed_projects(sort_by="latest", page=1, per_page=20):
        query = Project.query.filter_by(stage="completed")

        if sort_by == "oldest":
            query = query.order_by(Project.updated_at.asc())
        else:
            query = query.order_by(Project.updated_at.desc())

        pagination = query.paginate(page=page, per_page=per_page, error_out=False)
        return {
            "items": [p.to_dict() for p in pagination.items],
            "total": pagination.total,
            "page": pagination.page,
            "pages": pagination.pages,
            "per_page": pagination.per_page,
        }, None