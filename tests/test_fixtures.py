from flask import url_for
from gendb.models import User


class TestEndpoints:

    def test_home_bp_index(self, client):
        assert client.get(url_for('home_bp.index')).status == '200 OK'

    def test_home_bp_register(self, client):
        assert client.get(url_for('home_bp.register')).status == '200 OK'

    def test_home_bp_login(self, client):
        assert client.get(url_for('home_bp.login')).status == '200 OK'


class TestDB:

    def test_db(self, session):
        u = User(email='a@a.b')

        session.add(u)
        session.commit()

        assert u.id > 0

        get_u = User.query.all()

        assert get_u[0].email == 'a@a.b'
