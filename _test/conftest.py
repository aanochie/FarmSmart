import pytest
from app import create_app


@pytest.fixture()
def testapp():
    app = create_app()
    app.config['TESTING'] = True
    app.config['DEBUG'] = False
    with app.app_context():
        yield app


