import pytest
from gendb.app import create_app


@pytest.fixture
def app():
    app = create_app()
    return app


@pytest.fixture
def test_app(client):
    assert client.get(url_for('home_bp.index')).status_code == 200
