import pytest
from dbSetup import User
from app import app


@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client


def test_new_user(client):
    """
    Test function to check if the user is created and the password is hashed correctly.
    client: The Flask test client.
    Expected result: Pass
    """
    user = User('test@test.com', 'Testing123', 'johnny'
                , 'test', 'user')
    assert user.email == 'test@test.com'
    assert user.password != 'Testing123'
