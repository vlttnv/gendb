from flask import url_for


class TestFixtures:

    def test_home_bp_index(self, client):
        assert client.get(url_for('home_bp.index')).status == '200 OK'

    def test_home_bp_register(self, client):
        assert client.get(url_for('home_bp.register')).status == '200 OK'
