import pytest
from app import app


@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client


def test_search(client):
    """
    Test function to check if the /search route returns the search page.
    client: The Flask test client.
    Expected result: Pass
    """
    response = client.get('/search')
    print(response.data)
    assert b'<title>Search</title>' in response.data
