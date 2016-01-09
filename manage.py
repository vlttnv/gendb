import os.path

import argparse
import imp
from migrate.versioning import api

from gendb import create_app
from gendb.extensions import db
from config import SQLALCHEMY_DATABASE_URI
from config import SQLALCHEMY_MIGRATE_REPO

gendb = create_app()


parser = argparse.ArgumentParser(description='GenDB manager.')
parser.add_argument('-a', '--action', type=str,  help='Action to perform.')
parser.add_argument('-hs', '--host', type=str, default='0.0.0.0', help='Address to bind to.')


def db_action(h, db):
    if db == 'create':
        db_create()
    elif db == 'migrate':
        db_migrate()
    elif db == 'upgrade':
        db_upgrade()
    else:
        run(h)


def db_create():
    with gendb.app_context():
        db.create_all()
    if not os.path.exists(SQLALCHEMY_MIGRATE_REPO):
        api.create(SQLALCHEMY_MIGRATE_REPO, 'database repository')
        api.version_control(
            SQLALCHEMY_DATABASE_URI,
            SQLALCHEMY_MIGRATE_REPO
        )
    else:
        api.version_control(
            SQLALCHEMY_DATABASE_URI,
            SQLALCHEMY_MIGRATE_REPO,
            api.version(SQLALCHEMY_MIGRATE_REPO)
        )


def db_migrate():
    v = api.db_version(SQLALCHEMY_DATABASE_URI, SQLALCHEMY_MIGRATE_REPO)
    migration = (
        SQLALCHEMY_MIGRATE_REPO
        + ('/versions/%03d_migration.py' % (v + 1))
    )
    tmp_module = imp.new_module('old_model')
    old_model = api.create_model(
        SQLALCHEMY_DATABASE_URI,
        SQLALCHEMY_MIGRATE_REPO
    )
    exec(old_model, tmp_module.__dict__)
    script = api.make_update_script_for_model(
        SQLALCHEMY_DATABASE_URI,
        SQLALCHEMY_MIGRATE_REPO,
        tmp_module.meta,
        db.metadata
    )
    open(migration, "wt").write(script)
    api.upgrade(SQLALCHEMY_DATABASE_URI, SQLALCHEMY_MIGRATE_REPO)
    v = api.db_version(SQLALCHEMY_DATABASE_URI, SQLALCHEMY_MIGRATE_REPO)
    print('New migration saved as ' + migration)
    print('Current database version: ' + str(v))


def db_upgrade():
    api.upgrade(SQLALCHEMY_DATABASE_URI, SQLALCHEMY_MIGRATE_REPO)
    v = api.db_version(SQLALCHEMY_DATABASE_URI, SQLALCHEMY_MIGRATE_REPO)
    print('Current database version: ' + str(v))


def run(h):
    gendb.run(debug=True, threaded=True, host=h)


if __name__ == "__main__":
    args = parser.parse_args()
    db_action(args.host, args.action)
