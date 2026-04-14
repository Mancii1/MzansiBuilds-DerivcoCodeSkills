from datetime import datetime
from sqlalchemy import case
from app.extensions import db
from app.models import Milestone, Project


class MilestoneService:
    @staticmethod
    def create_milestone(project_id, user_id, data):
        """Create a new milestone for a project (owner only)."""
        project = db.session.get(Project, project_id)
        if not project:
            return None, "Project not found"
        if project.user_id != user_id:
            return None, "You do not have permission to add milestones to this project"

        if "title" not in data or not data["title"]:
            return None, "Title is required"

        # Parse due_date if provided
        due_date = None
        if "due_date" in data and data["due_date"]:
            try:
                due_date = datetime.strptime(data["due_date"], "%Y-%m-%d").date()
            except ValueError:
                return None, "Invalid due_date format. Use YYYY-MM-DD"

        milestone = Milestone(
            title=data["title"],
            project_id=project_id,
            description=data.get("description"),
            due_date=due_date
        )
        db.session.add(milestone)
        db.session.commit()
        return milestone, None

    @staticmethod
    def get_milestones_for_project(project_id):
        """Return all milestones for a project, ordered by due date (nulls last) and created date."""
        project = db.session.get(Project, project_id)
        if not project:
            return None, "Project not found"

        milestones = Milestone.query.filter_by(project_id=project_id).order_by(
            case((Milestone.due_date == None, 1), else_=0),  # NULLs last
            Milestone.due_date.asc(),
            Milestone.created_at.asc()
        ).all()
        return [m.to_dict() for m in milestones], None

    @staticmethod
    def update_milestone(milestone_id, user_id, data):
        """Update milestone details (owner only)."""
        milestone = db.session.get(Milestone, milestone_id)
        if not milestone:
            return None, "Milestone not found"
        if milestone.project.user_id != user_id:
            return None, "You do not have permission to update this milestone"

        updatable_fields = ["title", "description", "due_date"]
        for field in updatable_fields:
            if field in data:
                if field == "due_date" and data[field]:
                    try:
                        setattr(milestone, field, datetime.strptime(data[field], "%Y-%m-%d").date())
                    except ValueError:
                        return None, "Invalid due_date format. Use YYYY-MM-DD"
                else:
                    setattr(milestone, field, data[field])

        db.session.commit()
        return milestone, None

    @staticmethod
    def delete_milestone(milestone_id, user_id):
        """Delete a milestone (owner only)."""
        milestone = db.session.get(Milestone, milestone_id)
        if not milestone:
            return None, "Milestone not found"
        if milestone.project.user_id != user_id:
            return None, "You do not have permission to delete this milestone"

        db.session.delete(milestone)
        db.session.commit()
        return True, None

    @staticmethod
    def toggle_complete(milestone_id, user_id):
        """Toggle the completed status of a milestone (owner only)."""
        milestone = db.session.get(Milestone, milestone_id)
        if not milestone:
            return None, "Milestone not found"
        if milestone.project.user_id != user_id:
            return None, "You do not have permission to update this milestone"

        milestone.completed = not milestone.completed
        db.session.commit()
        return milestone, None

    @staticmethod
    def get_progress(project_id):
        """Return completion progress for a project: completed, total, percentage."""
        project = db.session.get(Project, project_id)
        if not project:
            return None, "Project not found"

        total = project.milestones.count()
        completed = project.milestones.filter_by(completed=True).count()
        percentage = (completed / total * 100) if total > 0 else 0
        return {
            "total": total,
            "completed": completed,
            "percentage": round(percentage, 2)
        }, None