from flask_jwt_extended import create_access_token, create_refresh_token
from app.extensions import db
from app.models import User


class AuthService:
    """Handles authentication business logic."""

    @staticmethod
    def register_user(email, username, password):
        """Register a new user."""
        # Normalise inputs
        email = email.lower().strip()
        username = username.strip()

        # Check if user already exists
        if User.query.filter((User.email == email) | (User.username == username)).first():
            return None, "User with that email or username already exists"

        # Create and save user
        user = User(email=email, username=username, password=password)
        db.session.add(user)
        db.session.commit()

        return user, None

    @staticmethod
    def login_user(identifier, password):
        """
        Authenticate a user by email or username.
        Returns (user, access_token, refresh_token) or (None, error_message).
        """
        # Find user by email or username
        user = User.query.filter(
            (User.email == identifier.lower().strip()) |
            (User.username == identifier.strip())
        ).first()

        if not user or not user.check_password(password):
            return None, None, None, "Invalid credentials"

        # Create tokens
        access_token = create_access_token(identity=str(user.id))
        refresh_token = create_refresh_token(identity=str(user.id))

        return user, access_token, refresh_token, None

    @staticmethod
    def refresh_access_token(user_id):
        """Generate a new access token from a valid refresh token."""
        user = User.query.get(user_id)
        if not user:
            return None, "User not found"
        access_token = create_access_token(identity=str(user.id))
        return access_token, None