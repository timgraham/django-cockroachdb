import subprocess
import sys

from django.db.backends.postgresql.creation import (
    DatabaseCreation as PostgresDatabaseCreation,
)

from .client import DatabaseClient


class DatabaseCreation(PostgresDatabaseCreation):

    def _clone_test_db(self, suffix, verbosity, keepdb=False):
        source_database_name = self.connection.settings_dict['NAME']
        target_database_name = self.get_test_db_clone_settings(suffix)['NAME']
        test_db_params = {
            'dbname': self.connection.ops.quote_name(target_database_name),
            'suffix': self.sql_table_creation_suffix(),
        }
        with self._nodb_cursor() as cursor:
            try:
                self._execute_create_test_db(cursor, test_db_params, keepdb)
            except Exception:
                if keepdb:
                    # If the database should be kept, skip everything else.
                    return
                try:
                    if verbosity >= 1:
                        self.log('Destroying old test database for alias %s...' % (
                            self._get_database_display_str(verbosity, target_database_name),
                        ))
                    cursor.execute('DROP DATABASE %(dbname)s' % test_db_params)
                    self._execute_create_test_db(cursor, test_db_params, keepdb)
                except Exception as e:
                    self.log('Got an error recreating the test database: %s' % e)
                    sys.exit(2)
        self._clone_db(source_database_name, target_database_name)

    def _clone_db(self, source_database_name, target_database_name):
        connect_args, env = DatabaseClient.settings_to_cmd_args_env(self.connection.settings_dict, [])
        # Chop off ['cockroach', 'sql', '--database=test_djangotests', ...]
        connect_args = connect_args[3:]
        dump_cmd = ['cockroach', 'dump', source_database_name] + connect_args
        load_cmd = ['cockroach', 'sql', '-d', target_database_name] + connect_args
        with subprocess.Popen(dump_cmd, stdout=subprocess.PIPE, env=env) as dump_proc:
            with subprocess.Popen(load_cmd, stdin=dump_proc.stdout, stdout=subprocess.DEVNULL, env=env):
                # Allow dump_proc to receive a SIGPIPE if the load process exits.
                dump_proc.stdout.close()
