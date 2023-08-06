from backup_tool.providers.backup import BackupProvider
import logging
from backup_tool import util
import psycopg2
import os
import subprocess

log = logging.getLogger("MysqldumpBackupProvider")


class PostgresqlBackupProvider(BackupProvider):

    def __init__(self, provider_config: dict):
        self._host = util.require_not_null(provider_config["host"], "host")
        self._password = util.require_not_null(provider_config["password"], "password")
        self._user = util.require_not_null(provider_config["user"], "user")

        if "allDatabases" in provider_config:
            self._all_databases = provider_config["allDatabases"]
            if self._all_databases and "databases" in provider_config:
                raise ValueError("'databases' list is not allowed when 'allDatabases=true'")
        else:
            self._databases = util.require_not_null(provider_config["databases"], "databases")

    def backup(self, out_file: str, tmp_dir: str):
        log.info("starting backup with pg_dump")
        if self._all_databases:
            self.backup_all_databases(tmp_dir)
        else:
            for database in self._databases:
                self.backup_database(tmp_dir, database)

        util.zipdir(out_file, tmp_dir)

    def backup_all_databases(self, tmp_dir: str):
        conn = psycopg2.connect(
            "user='{user}' host='{host}' password='{password}'".format(user=self._user, host=self._host,
                                                                       password=self._password))
        cur = conn.cursor()
        cur.execute("select datname from pg_database;")
        databases = list(map(lambda x: x[0], cur.fetchall()))
        cur.close()
        conn.close()
        for database in databases:
            self.backup_database(tmp_dir, database)

    def backup_database(self, tmp_dir: str, database: str):
        log.info("backing up database {name}".format(name=database))
        with open(os.path.join(tmp_dir, database + ".sql"), "w") as outfile:
            subprocess.run(["pg_dump", "-h", self._host, "-U", self._user, database],
                           stdout=outfile, env={**os.environ, "PGPASSWORD": self._password})

    @classmethod
    def get_provider_key(cls) -> str:
        return "postgresql"
