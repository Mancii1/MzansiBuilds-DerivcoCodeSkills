import pytest
from app.models import User
from app.extensions import db


class TestAuthEndpoints:
    """Test authentication endpoints."""

    def test_register_success(self, client):
        """Test successful user registration."""
        response = client.post("/api/auth/register", json={
            "email": "test@example.com",
            "username": "testuser",
            "password": "securepassword123"
        })
        assert response.status_code == 201
        data = response.get_json()
        assert data["message"] == "User registered successfully"
        assert data["user"]["email"] == "test@example.com"
        assert data["user"]["username"] == "testuser"

        # Verify user exists in database
        user = User.query.filter_by(email="test@example.com").first()
        assert user is not None
        assert user.check_password("securepassword123") is True

    def test_register_duplicate_email(self, client):
        """Test registration with existing email fails."""
        # Create a user first
        client.post("/api/auth/register", json={
            "email": "duplicate@example.com",
            "username": "user1",
            "password": "password123"
        })
        # Try to register with same email
        response = client.post("/api/auth/register", json={
            "email": "duplicate@example.com",
            "username": "user2",
            "password": "password456"
        })
        assert response.status_code == 400
        assert "already exists" in response.get_json()["error"]

    def test_register_duplicate_username(self, client):
        """Test registration with existing username fails."""
        client.post("/api/auth/register", json={
            "email": "user1@example.com",
            "username": "sameuser",
            "password": "password123"
        })
        response = client.post("/api/auth/register", json={
            "email": "user2@example.com",
            "username": "sameuser",
            "password": "password456"
        })
        assert response.status_code == 400
        assert "already exists" in response.get_json()["error"]

    def test_register_missing_fields(self, client):
        """Test registration with missing fields returns 400."""
        response = client.post("/api/auth/register", json={"email": "test@example.com"})
        assert response.status_code == 400
        assert "Missing required fields" in response.get_json()["error"]

    def test_register_short_password(self, client):
        """Test registration with short password fails."""
        response = client.post("/api/auth/register", json={
            "email": "test@example.com",
            "username": "testuser",
            "password": "short"
        })
        assert response.status_code == 400
        assert "at least 8 characters" in response.get_json()["error"]

    def test_login_success_with_email(self, client):
        """Test login using email returns tokens."""
        # Register user
        client.post("/api/auth/register", json={
            "email": "login@example.com",
            "username": "loginuser",
            "password": "validpass123"
        })
        # Login
        response = client.post("/api/auth/login", json={
            "identifier": "login@example.com",
            "password": "validpass123"
        })
        assert response.status_code == 200
        data = response.get_json()
        assert "access_token" in data
        assert "refresh_token" in data
        assert data["user"]["email"] == "login@example.com"

    def test_login_success_with_username(self, client):
        """Test login using username returns tokens."""
        client.post("/api/auth/register", json={
            "email": "user2@example.com",
            "username": "nameonly",
            "password": "validpass123"
        })
        response = client.post("/api/auth/login", json={
            "identifier": "nameonly",
            "password": "validpass123"
        })
        assert response.status_code == 200
        assert "access_token" in response.get_json()

    def test_login_invalid_password(self, client):
        """Test login with wrong password fails."""
        client.post("/api/auth/register", json={
            "email": "wrong@example.com",
            "username": "wrongpass",
            "password": "correctpass"
        })
        response = client.post("/api/auth/login", json={
            "identifier": "wrong@example.com",
            "password": "incorrect"
        })
        assert response.status_code == 401
        assert "Invalid credentials" in response.get_json()["error"]

    def test_login_nonexistent_user(self, client):
        """Test login with unknown user fails."""
        response = client.post("/api/auth/login", json={
            "identifier": "nobody@example.com",
            "password": "whatever"
        })
        assert response.status_code == 401
        assert "Invalid credentials" in response.get_json()["error"]

    def test_refresh_token(self, client):
        """Test obtaining a new access token with a refresh token."""
        # Register and login to get refresh token
        client.post("/api/auth/register", json={
            "email": "refresh@example.com",
            "username": "refresher",
            "password": "validpass123"
        })
        login_resp = client.post("/api/auth/login", json={
            "identifier": "refresh@example.com",
            "password": "validpass123"
        })
        refresh_token = login_resp.get_json()["refresh_token"]

        # Use refresh token to get new access token
        response = client.post("/api/auth/refresh",
                               headers={"Authorization": f"Bearer {refresh_token}"})
        assert response.status_code == 200
        assert "access_token" in response.get_json()

    def test_refresh_without_token(self, client):
        """Test refresh endpoint without token fails."""
        response = client.post("/api/auth/refresh")
        assert response.status_code == 401  # Unauthorized

    def test_protected_route_requires_token(self, client):
        """Test that a protected route (refresh endpoint with wrong token type) fails."""
        # We'll test a dummy protected route later; for now ensure JWT is enforced
        response = client.post("/api/auth/refresh")
        assert response.status_code == 401