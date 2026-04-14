from app.routes.auth import auth_bp
from app.routes.profile import profile_bp
from app.routes.projects import projects_bp
from app.routes.comments import comments_bp
from app.routes.likes import likes_bp
from app.routes.collaborations import collaborations_bp
from app.routes.milestones import milestones_bp

__all__ = ["auth_bp", "profile_bp", "projects_bp", "comments_bp", "likes_bp", "collaborations_bp", "milestones_bp"]