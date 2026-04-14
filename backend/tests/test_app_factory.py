def test_app_creation(app):
    """Test that the app is created with testing config."""
    assert app.config["TESTING"] is True
    assert app.config["SQLALCHEMY_DATABASE_URI"] is not None


def test_health_endpoint(client):
    """Test the health check endpoint."""
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json == {"status": "ok"}


def test_404_returns_json(client):
    """Test that HTTP exceptions are returned as JSON."""
    response = client.get("/nonexistent")
    assert response.status_code == 404
    assert response.content_type == "application/json"
    assert "code" in response.json