from flask import url_for
from sqlalchemy.orm.exc import NoResultFound

from gendb.models import User


class TestEndpoints:

    def test_home_bp_index(self, client):
        assert client.get(url_for('home_bp.index')).status == '302 FOUND'

    def test_home_bp_register(self, client):
        assert client.get(url_for('home_bp.register')).status == '200 OK'

    def test_home_bp_login(self, client):
        assert client.get(url_for('home_bp.login')).status == '200 OK'


class TestUserAuth():

    def test_register(self, client, session):
        l = client.post(
            url_for('home_bp.register'),
            data={
                'email': 'test@test.com',
                'pw1': 'password123',
                'pw2': 'password123'
            },
            follow_redirects=True
        )

        assert 'Log out' in str(l.data)

        try:
            u = User.query.filter_by(email='test@test.com').one()
            assert u.email == 'test@test.com'
        except NoResultFound:
            raise

    def test_login(self, client, session):
        l = client.post(
            url_for('home_bp.login'),
            data={
                'email': 'test@test.com',
                'pw1': 'password123',
            },
            follow_redirects=True
        )

        assert 'Log out' in str(l.data)

    def test_wrong_login(self, client, session):
        l = client.post(
            url_for('home_bp.login'),
            data={
                'email': 'test@test.com',
                'pw1': 'wrong_pass',
            },
            follow_redirects=True
        )

        assert 'Incorrect' in str(l.data)

        l = client.post(
            url_for('home_bp.login'),
            data={
                'email': 'wrong@test.com',
                'pw1': 'password123',
            },
            follow_redirects=True
        )

        assert 'User not found' in str(l.data)

    def test_create_project(self, client, session):
        l = client.get(url_for('projects_bp.projects'))

        assert '302 FOUND' == l.status
        assert '<h1>Projects</h1>' not in str(l.data)

        l = client.post(
            url_for('home_bp.login'),
            data={
                'email': 'test@test.com',
                'pw1': 'password123',
            },
            follow_redirects=True
        )

        assert 'Log out' in str(l.data)

        l = client.get(url_for('projects_bp.projects'))

        assert '200 OK' == l.status
        assert 'Add Project' in str(l.data)

    def test_logout(self, client, session):
        l = client.get(
            url_for('home_bp.logout'),
            follow_redirects=True
        )

        assert 'Log In' in str(l.data)
