# test_check.py

import pytest
from flaskBlog import app

@pytest.fixture
def client():
    """Create a test client for the app."""
    with app.test_client() as client:
        yield client

def test_home_page(client):
    """Test the home page route."""
    response = client.get('/')
    assert response.status_code == 200
    assert b'TukTuk Blog' in response.data
    assert b'Food Blog post' in response.data

def test_about_page(client):
    """Test the about page route."""
    response = client.get('/about')
    assert response.status_code == 200
    assert b'About' in response.data

# Add more tests as needed for other routes and functionalities
