import pytest
from app.models import User, Skill
from app.extensions import db


class TestProfileEndpoints:
    """Test profile-related endpoints."""

    @pytest.fixture
    def auth_headers(self, client):
        """Register and login a test user, return auth headers."""
        client.post("/api/auth/register", json={
            "email": "profile@test.com",
            "username": "profileuser",
            "password": "password123"
        })
        login_resp = client.post("/api/auth/login", json={
            "identifier": "profileuser",
            "password": "password123"
        })
        token = login_resp.get_json()["access_token"]
        return {"Authorization": f"Bearer {token}"}

    def test_get_own_profile_unauthenticated(self, client):
        """Test that unauthenticated request is rejected."""
        response = client.get("/api/profile")
        assert response.status_code == 401

    def test_get_own_profile(self, client, auth_headers):
        """Test authenticated user can retrieve own profile."""
        response = client.get("/api/profile", headers=auth_headers)
        assert response.status_code == 200
        data = response.get_json()
        assert data["username"] == "profileuser"
        assert data["email"] == "profile@test.com"
        assert "skills" in data

    def test_update_profile_bio(self, client, auth_headers):
        """Test updating bio field."""
        response = client.put("/api/profile", json={
            "bio": "Full-stack developer from Cape Town"
        }, headers=auth_headers)
        assert response.status_code == 200
        data = response.get_json()
        assert data["bio"] == "Full-stack developer from Cape Town"

    def test_update_profile_skills(self, client, auth_headers):
        """Test adding skills."""
        response = client.put("/api/profile", json={
            "skills": ["Python", "Flask", "React"]
        }, headers=auth_headers)
        assert response.status_code == 200
        data = response.get_json()
        assert set(data["skills"]) == {"python", "flask", "react"}

        # Verify skills were created in database
        skills = Skill.query.all()
        assert len(skills) == 3

    def test_update_profile_invalid_field(self, client, auth_headers):
        """Test that unknown fields are rejected."""
        response = client.put("/api/profile", json={
            "invalid_field": "should not work"
        }, headers=auth_headers)
        assert response.status_code == 400
        assert "Invalid fields" in response.get_json()["error"]

    def test_get_public_profile(self, client, auth_headers):
        """Test public profile view does not expose email."""
        # First update some profile data
        client.put("/api/profile", json={
            "bio": "Public bio",
            "location": "Johannesburg"
        }, headers=auth_headers)

        # Get user ID from own profile
        own_profile = client.get("/api/profile", headers=auth_headers).get_json()
        user_id = own_profile["id"]

        # Public request (no auth)
        response = client.get(f"/api/users/{user_id}")
        assert response.status_code == 200
        data = response.get_json()
        assert "email" not in data
        assert data["bio"] == "Public bio"
        assert data["username"] == "profileuser"

    def test_get_public_profile_nonexistent(self, client):
        """Test 404 for non-existent user."""
        response = client.get("/api/users/9999")
        assert response.status_code == 404

print("Loading test_profile.py")