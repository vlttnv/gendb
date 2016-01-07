import os.path

import click
import imp
from migrate.versioning import api

from gendb import create_app
from gendb.extensions import db
from config import SQLALCHEMY_DATABASE_URI
from config import SQLALCHEMY_MIGRATE_REPO

gendb = create_app()


@click.group()
def app():
    return


@app.command()
def run():
    gendb.run(debug=True, threaded=True, host='0.0.0.0')


@app.command()
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


@app.command()
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


@app.command()
def db_upgrade():
    api.upgrade(SQLALCHEMY_DATABASE_URI, SQLALCHEMY_MIGRATE_REPO)
    v = api.db_version(SQLALCHEMY_DATABASE_URI, SQLALCHEMY_MIGRATE_REPO)
    print('Current database version: ' + str(v))


if __name__ == "__main__":
    app()
