import pytest
from app.models import Milestone
from app.extensions import db


class TestMilestones:
    @pytest.fixture
    def owner_headers(self, client):
        """Register and login project owner."""
        client.post("/api/auth/register", json={
            "email": "owner@test.com",
            "username": "owner",
            "password": "password123"
        })
        login_resp = client.post("/api/auth/login", json={
            "identifier": "owner",
            "password": "password123"
        })
        token = login_resp.get_json()["access_token"]
        return {"Authorization": f"Bearer {token}"}

    @pytest.fixture
    def other_headers(self, client):
        """Non-owner user."""
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
    def sample_project(self, client, owner_headers):
        """Create a project owned by 'owner'."""
        resp = client.post("/api/projects", json={
            "title": "Milestone Test Project",
            "description": "Testing milestones"
        }, headers=owner_headers)
        return resp.get_json()["id"]

    def test_create_milestone_unauthenticated(self, client, sample_project):
        response = client.post(f"/api/projects/{sample_project}/milestones", json={"title": "M1"})
        assert response.status_code == 401

    def test_create_milestone_success(self, client, owner_headers, sample_project):
        response = client.post(f"/api/projects/{sample_project}/milestones", json={
            "title": "First Milestone",
            "description": "Do the thing",
            "due_date": "2025-12-31"
        }, headers=owner_headers)
        assert response.status_code == 201
        data = response.get_json()
        assert data["title"] == "First Milestone"
        assert data["due_date"] == "2025-12-31"
        assert data["completed"] is False

    def test_create_milestone_non_owner_fails(self, client, other_headers, sample_project):
        response = client.post(f"/api/projects/{sample_project}/milestones", json={"title": "Hack"}, headers=other_headers)
        assert response.status_code == 403

    def test_create_milestone_missing_title(self, client, owner_headers, sample_project):
        response = client.post(f"/api/projects/{sample_project}/milestones", json={}, headers=owner_headers)
        assert response.status_code == 400
        assert "Title is required" in response.get_json()["error"]

    def test_create_milestone_missing_title(self, client, owner_headers, sample_project):
        response = client.post(f"/api/projects/{sample_project}/milestones", json={"description": "No title provided"}, headers=owner_headers)
        assert response.status_code == 400
        assert "Title is required" in response.get_json()["error"]

    def test_get_milestones(self, client, owner_headers, sample_project):
        # Create two milestones
        client.post(f"/api/projects/{sample_project}/milestones", json={"title": "M1"}, headers=owner_headers)
        client.post(f"/api/projects/{sample_project}/milestones", json={"title": "M2"}, headers=owner_headers)
        response = client.get(f"/api/projects/{sample_project}/milestones")
        assert response.status_code == 200
        data = response.get_json()
        assert len(data) == 2
        assert data[0]["title"] == "M1"

    def test_update_milestone_owner(self, client, owner_headers, sample_project):
        # Create milestone
        resp = client.post(f"/api/projects/{sample_project}/milestones", json={"title": "Old"}, headers=owner_headers)
        milestone_id = resp.get_json()["id"]
        # Update
        update_resp = client.put(f"/api/projects/milestones/{milestone_id}", json={"title": "New Title"}, headers=owner_headers)
        assert update_resp.status_code == 200
        assert update_resp.get_json()["title"] == "New Title"

    def test_update_milestone_non_owner_fails(self, client, owner_headers, other_headers, sample_project):
        resp = client.post(f"/api/projects/{sample_project}/milestones", json={"title": "Secure"}, headers=owner_headers)
        milestone_id = resp.get_json()["id"]
        response = client.put(f"/api/projects/milestones/{milestone_id}", json={"title": "Hacked"}, headers=other_headers)
        assert response.status_code == 403

    def test_delete_milestone_owner(self, client, owner_headers, sample_project):
        resp = client.post(f"/api/projects/{sample_project}/milestones", json={"title": "Delete me"}, headers=owner_headers)
        milestone_id = resp.get_json()["id"]
        del_resp = client.delete(f"/api/projects/milestones/{milestone_id}", headers=owner_headers)
        assert del_resp.status_code == 200
        # Verify gone
        get_resp = client.get(f"/api/projects/{sample_project}/milestones")
        assert len(get_resp.get_json()) == 0

    def test_toggle_complete(self, client, owner_headers, sample_project):
        resp = client.post(f"/api/projects/{sample_project}/milestones", json={"title": "Toggle"}, headers=owner_headers)
        milestone_id = resp.get_json()["id"]
        # Complete
        toggle = client.patch(f"/api/projects/milestones/{milestone_id}/toggle", headers=owner_headers)
        assert toggle.status_code == 200
        assert toggle.get_json()["completed"] is True
        # Uncomplete
        toggle2 = client.patch(f"/api/projects/milestones/{milestone_id}/toggle", headers=owner_headers)
        assert toggle2.get_json()["completed"] is False

    def test_get_progress(self, client, owner_headers, sample_project):
        # Create two milestones
        m1 = client.post(f"/api/projects/{sample_project}/milestones", json={"title": "M1"}, headers=owner_headers).get_json()["id"]
        m2 = client.post(f"/api/projects/{sample_project}/milestones", json={"title": "M2"}, headers=owner_headers).get_json()["id"]
        # Complete one
        client.patch(f"/api/projects/milestones/{m1}/toggle", headers=owner_headers)
        # Check progress
        response = client.get(f"/api/projects/{sample_project}/progress")
        assert response.status_code == 200
        data = response.get_json()
        assert data["total"] == 2
        assert data["completed"] == 1
        assert data["percentage"] == 50.0