import pytest

from app import app


@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client


def test_homepage(client):
    """
    Test function to check if the homepage '/' route returns the correct title.
    client: The Flask test client.
    Expected result: Pass
    """
    response = client.get('/')
    assert b'<title>CSC2033</title>' in response.data


def test_homepage_post(client):
    """
    Test function to check if posting to the homepage '/' route returns a 405 Method Not Allowed error.
    client: The Flask test client.
    Expected result: Pass
    """
    response = client.post('/')
    assert response.status_code == 405