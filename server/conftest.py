# server/conftest.py
#!/usr/bin/env python3
import pytest
from app import app
from models import *

@pytest.fixture(scope="function")
def test_client():
    # Configure the app for testing
    app.config["TESTING"] = True
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///:memory:"
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

    with app.app_context():
        # Create all tables
        db.create_all()

        # Yield the test client
        yield app.test_client()

        # Clean up after each test
        db.session.remove()
        db.drop_all()