import os.path
import sys

import imp
from migrate.versioning import api

from gendb import create_app
from gendb.extensions import db
from config import SQLALCHEMY_DATABASE_URI
from config import SQLALCHEMY_MIGRATE_REPO

gendb = create_app()

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print('Wrong!')
        sys.exit(1)
    elif sys.argv[1] == 'run':
        print('Run.')
        gendb.run(debug=True, threaded=True, host='0.0.0.0')
    elif sys.argv[1] == 'db_create':
        print('DB create.')
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
    elif sys.argv[1] == 'db_migrate':
        print('DB migrate.')
        v = api.db_version(SQLALCHEMY_DATABASE_URI, SQLALCHEMY_MIGRATE_REPO)
        migration = (SQLALCHEMY_MIGRATE_REPO
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
    elif sys.argv[1] == 'db_upgrade':
        print('DB migrate')
        api.upgrade(SQLALCHEMY_DATABASE_URI, SQLALCHEMY_MIGRATE_REPO)
        v = api.db_version(SQLALCHEMY_DATABASE_URI, SQLALCHEMY_MIGRATE_REPO)
        print('Current database version: ' + str(v))
