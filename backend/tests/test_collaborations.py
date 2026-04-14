import pytest
from app.models import CollaborationRequest
from app.extensions import db


class TestCollaborationRequests:
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
    def requester_headers(self, client):
        """Register and login a user who will request collaboration."""
        client.post("/api/auth/register", json={
            "email": "requester@test.com",
            "username": "requester",
            "password": "password123"
        })
        login_resp = client.post("/api/auth/login", json={
            "identifier": "requester",
            "password": "password123"
        })
        token = login_resp.get_json()["access_token"]
        return {"Authorization": f"Bearer {token}"}

    @pytest.fixture
    def another_headers(self, client):
        """Third user for edge cases."""
        client.post("/api/auth/register", json={
            "email": "another@test.com",
            "username": "another",
            "password": "password123"
        })
        login_resp = client.post("/api/auth/login", json={
            "identifier": "another",
            "password": "password123"
        })
        token = login_resp.get_json()["access_token"]
        return {"Authorization": f"Bearer {token}"}

    @pytest.fixture
    def sample_project(self, client, owner_headers):
        """Create a project owned by 'owner'."""
        resp = client.post("/api/projects", json={
            "title": "Collab Project",
            "description": "Looking for help"
        }, headers=owner_headers)
        return resp.get_json()["id"]

    def test_request_collaboration_unauthenticated(self, client, sample_project):
        response = client.post(f"/api/projects/{sample_project}/collaborate", json={"message": "I want to help"})
        assert response.status_code == 401

    def test_request_collaboration_success(self, client, requester_headers, sample_project):
        response = client.post(f"/api/projects/{sample_project}/collaborate",
                               json={"message": "I can help with testing"},
                               headers=requester_headers)
        assert response.status_code == 201
        data = response.get_json()
        assert data["status"] == "pending"
        assert data["project_id"] == sample_project
        assert data["requester_username"] == "requester"

    def test_cannot_request_own_project(self, client, owner_headers, sample_project):
        response = client.post(f"/api/projects/{sample_project}/collaborate",
                               json={"message": "Self collab"},
                               headers=owner_headers)
        assert response.status_code == 400
        assert "own project" in response.get_json()["error"]

    def test_cannot_duplicate_pending_request(self, client, requester_headers, sample_project):
        # First request
        client.post(f"/api/projects/{sample_project}/collaborate", json={"message": "First"}, headers=requester_headers)
        # Duplicate
        response = client.post(f"/api/projects/{sample_project}/collaborate", json={"message": "Second"}, headers=requester_headers)
        assert response.status_code == 400
        assert "already have" in response.get_json()["error"]

    def test_get_incoming_requests(self, client, owner_headers, requester_headers, sample_project):
        # Send request
        client.post(f"/api/projects/{sample_project}/collaborate", json={"message": "Help"}, headers=requester_headers)
        # Owner fetches incoming
        response = client.get("/api/collaborations/incoming", headers=owner_headers)
        assert response.status_code == 200
        data = response.get_json()
        assert len(data) == 1
        assert data[0]["status"] == "pending"

    def test_get_outgoing_requests(self, client, requester_headers, sample_project):
        client.post(f"/api/projects/{sample_project}/collaborate", json={"message": "Sent"}, headers=requester_headers)
        response = client.get("/api/collaborations/outgoing", headers=requester_headers)
        assert response.status_code == 200
        data = response.get_json()
        assert len(data) == 1
        assert data[0]["status"] == "pending"

    def test_accept_request(self, client, owner_headers, requester_headers, sample_project):
        # Send request
        req_resp = client.post(f"/api/projects/{sample_project}/collaborate", json={"message": "Accept me"}, headers=requester_headers)
        request_id = req_resp.get_json()["id"]
        # Owner accepts
        response = client.patch(f"/api/collaborations/{request_id}/accept", headers=owner_headers)
        assert response.status_code == 200
        assert response.get_json()["status"] == "accepted"

    def test_reject_request(self, client, owner_headers, requester_headers, sample_project):
        req_resp = client.post(f"/api/projects/{sample_project}/collaborate", json={"message": "Reject me"}, headers=requester_headers)
        request_id = req_resp.get_json()["id"]
        response = client.patch(f"/api/collaborations/{request_id}/reject", headers=owner_headers)
        assert response.status_code == 200
        assert response.get_json()["status"] == "rejected"

    def test_cannot_accept_non_pending(self, client, owner_headers, requester_headers, sample_project):
        req_resp = client.post(f"/api/projects/{sample_project}/collaborate", json={"message": "Test"}, headers=requester_headers)
        request_id = req_resp.get_json()["id"]
        # Accept first
        client.patch(f"/api/collaborations/{request_id}/accept", headers=owner_headers)
        # Try to accept again
        response = client.patch(f"/api/collaborations/{request_id}/accept", headers=owner_headers)
        assert response.status_code == 400
        assert "already accepted" in response.get_json()["error"]

    def test_non_owner_cannot_manage_request(self, client, requester_headers, another_headers, sample_project):
        req_resp = client.post(f"/api/projects/{sample_project}/collaborate", json={"message": "Test"}, headers=requester_headers)
        request_id = req_resp.get_json()["id"]
        # Another user tries to accept
        response = client.patch(f"/api/collaborations/{request_id}/accept", headers=another_headers)
        assert response.status_code == 403
        assert "permission" in response.get_json()["error"].lower()