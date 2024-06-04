import pytest
from app import app


@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client


def test_forecast(client):
    """
    Test function to check if the /map route returns the map page.
    client: The Flask test client.
    Expected result: Pass
    """
    response = client.get('/forecast')
    assert b'<title>Weather App</title>' in response.data
