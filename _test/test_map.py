import pytest

from app import app


@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client


def test_map(client):
    """
    Test function to check if the /map route returns the map page.
    client: The Flask test client.
    Expected result: Pass
    """
    response = client.get('/map')
    assert b'<title>Regional Maps</title>' in response.data


def test_default_map_view(client):
    """
    Test function to check if the /map route returns the correct map.
    client: The Flask test client.
    Expected result: Pass
    """
    response = client.get('/map')
    assert b'static/images/ALC map.jpg' in response.data


def test_query_map_view(client):
    """
    Test function to check if the /map route returns the correct map.
    client: The Flask test client.
    Expected result: Pass
    """
    response = client.get('region', 'north-west-lands.jpg')
    assert b'north-west-lands.jpg' in response.data
