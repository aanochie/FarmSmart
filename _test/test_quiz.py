# test_app.py

import pytest
from app import app
from quiz.views import currentqid, maxid


@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client


def test_quiz(client):
    """
    Test function to check if the /quiz route returns the quiz page.
    client: The Flask test client.
    Expected result: Pass
    """
    response = client.get('/quiz')
    print(response.data)
    assert b'<title>Quiz</title>' in response.data


def test_qid(client):
    """
    Test to check if the selected QID is within an expected range
    client: The Flask test client.
    Expected result: Pass
    """
    assert 0 < currentqid <= maxid
