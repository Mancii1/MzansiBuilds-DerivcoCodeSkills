import pytest
from app import create_app
from app.extensions import db
from app.config import TestingConfig


@pytest.fixture(scope="function")  # Changed from session to function for isolation
def app():
    """Create and configure a Flask app for testing."""
    app = create_app("testing")
    with app.app_context():
        db.create_all()
        yield app
        db.session.remove()
        db.drop_all()


@pytest.fixture
def client(app):
    """A test client for the app."""
    return app.test_client()