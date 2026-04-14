import pytest
from app.models import Project, Comment
from app.extensions import db


class TestCommentsLikes:
    @pytest.fixture
    def auth_headers(self, client):
        """Register and login a test user, return auth headers."""
        client.post("/api/auth/register", json={
            "email": "testuser@test.com",
            "username": "testuser",
            "password": "password123"
        })
        login_resp = client.post("/api/auth/login", json={
            "identifier": "testuser",
            "password": "password123"
        })
        token = login_resp.get_json()["access_token"]
        return {"Authorization": f"Bearer {token}"}

    @pytest.fixture
    def other_headers(self, client):
        """Second user for permission tests."""
        client.post("/api/auth/register", json={
            "email": "other@test.com",
            "username": "otheruser",
            "password": "password123"
        })
        login_resp = client.post("/api/auth/login", json={
            "identifier": "otheruser",
            "password": "password123"
        })
        token = login_resp.get_json()["access_token"]
        return {"Authorization": f"Bearer {token}"}

    @pytest.fixture
    def sample_project(self, client, auth_headers):
        """Create a project and return its ID."""
        resp = client.post("/api/projects", json={
            "title": "Test Project",
            "description": "A project for testing comments and likes"
        }, headers=auth_headers)
        return resp.get_json()["id"]

    # --- Comments Tests ---
    def test_add_comment_unauthenticated(self, client, sample_project):
        response = client.post(f"/api/projects/{sample_project}/comments", json={
            "content": "Nice project!"
        })
        assert response.status_code == 401

    def test_add_comment_success(self, client, auth_headers, sample_project):
        response = client.post(f"/api/projects/{sample_project}/comments", json={
            "content": "Great work!"
        }, headers=auth_headers)
        assert response.status_code == 201
        data = response.get_json()
        assert data["content"] == "Great work!"
        assert data["author_username"] == "testuser"

    def test_get_comments(self, client, auth_headers, sample_project):
        # Add two comments
        client.post(f"/api/projects/{sample_project}/comments", json={"content": "First"}, headers=auth_headers)
        client.post(f"/api/projects/{sample_project}/comments", json={"content": "Second"}, headers=auth_headers)
        response = client.get(f"/api/projects/{sample_project}/comments")
        assert response.status_code == 200
        comments = response.get_json()
        assert len(comments) == 2
        assert comments[0]["content"] == "Second"  # newest first

    def test_delete_comment_owner(self, client, auth_headers, sample_project):
        # Add a comment
        resp = client.post(f"/api/projects/{sample_project}/comments", json={"content": "Delete me"}, headers=auth_headers)
        comment_id = resp.get_json()["id"]
        # Delete it
        del_resp = client.delete(f"/api/projects/comments/{comment_id}", headers=auth_headers)
        assert del_resp.status_code == 200
        # Verify it's gone
        get_resp = client.get(f"/api/projects/{sample_project}/comments")
        assert len(get_resp.get_json()) == 0

    def test_delete_comment_not_owner(self, client, auth_headers, other_headers, sample_project):
        # Owner adds comment
        resp = client.post(f"/api/projects/{sample_project}/comments", json={"content": "Owner comment"}, headers=auth_headers)
        comment_id = resp.get_json()["id"]
        # Other user tries to delete
        del_resp = client.delete(f"/api/projects/comments/{comment_id}", headers=other_headers)
        assert del_resp.status_code == 403

    # --- Likes Tests ---
    def test_toggle_like_unauthenticated(self, client, sample_project):
        response = client.post(f"/api/projects/{sample_project}/like")
        assert response.status_code == 401

    def test_like_project(self, client, auth_headers, sample_project):
        # Like
        resp = client.post(f"/api/projects/{sample_project}/like", headers=auth_headers)
        assert resp.status_code == 200
        assert resp.get_json()["liked"] is True
        # Check like count
        proj_resp = client.get(f"/api/projects/{sample_project}")
        assert proj_resp.get_json()["likes_count"] == 1

    def test_unlike_project(self, client, auth_headers, sample_project):
        # Like first
        client.post(f"/api/projects/{sample_project}/like", headers=auth_headers)
        # Unlike
        resp = client.post(f"/api/projects/{sample_project}/like", headers=auth_headers)
        assert resp.status_code == 200
        assert resp.get_json()["liked"] is False
        # Count back to 0
        proj_resp = client.get(f"/api/projects/{sample_project}")
        assert proj_resp.get_json()["likes_count"] == 0

    def test_get_likers(self, client, auth_headers, sample_project):
        client.post(f"/api/projects/{sample_project}/like", headers=auth_headers)
        resp = client.get(f"/api/projects/{sample_project}/likes")
        assert resp.status_code == 200
        data = resp.get_json()
        assert data["count"] == 1
        assert "testuser" in data["likers"]

    def test_feed_most_liked_sorting(self, client, auth_headers):
        # Create two projects
        p1 = client.post("/api/projects", json={"title": "P1", "description": "..."}, headers=auth_headers).get_json()["id"]
        p2 = client.post("/api/projects", json={"title": "P2", "description": "..."}, headers=auth_headers).get_json()["id"]
        # Like p2 twice (create second user)
        client.post("/api/auth/register", json={"email": "fan@test.com", "username": "fan", "password": "password123"})
        fan_login = client.post("/api/auth/login", json={"identifier": "fan", "password": "password123"})
        fan_token = fan_login.get_json()["access_token"]
        fan_headers = {"Authorization": f"Bearer {fan_token}"}
        client.post(f"/api/projects/{p2}/like", headers=auth_headers)
        client.post(f"/api/projects/{p2}/like", headers=fan_headers)
        # Feed sorted by most_liked
        resp = client.get("/api/projects/feed?sort=most_liked")
        items = resp.get_json()["items"]
        assert items[0]["id"] == p2
        assert items[1]["id"] == p1