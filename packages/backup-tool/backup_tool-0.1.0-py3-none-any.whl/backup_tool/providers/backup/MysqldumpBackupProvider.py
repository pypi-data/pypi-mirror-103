from backup_tool.providers.backup import BackupProvider
import backup_tool.util as util
import subprocess
import os
import logging

log = logging.getLogger("MysqldumpBackupProvider")


class MysqldumpBackupProvider(BackupProvider):

    def __init__(self, provider_config: dict):
        self._excluded_databases = ["information_schema", "performance_schema"]
        self._host = util.require_not_null(provider_config["host"], "host")
        self._password = util.require_not_null(provider_config["password"], "password")
        self._user = util.require_not_null(provider_config["user"], "user")

        if "allDatabases" in provider_config:
            self._all_databases = provider_config["allDatabases"]
            if self._all_databases and "databases" in provider_config:
                raise ValueError("'databases' list is not allowed when 'allDatabases=true'")
        else:
            self._databases = util.require_not_null(provider_config["databases"], "databases")

    def backup_database(self, tmp_dir: str, name: str):
        if name in self._excluded_databases:
            log.info("skipping {database_name}".format(database_name=name))
            return
        log.info("backing up database {name}".format(name=name))

        with open(os.path.join(tmp_dir, name + ".sql"), "w") as outfile:
            subprocess.run(["mysqldump", "-h", self._host, "-u", self._user, "-p" + self._password, name],
                           stdout=outfile)

    def backup_all_databases(self, tmp_dir: str):
        databases = subprocess.check_output(
            ["mysql", "-h", self._host, "-u", self._user, "-e", "show databases;", "-p" + self._password]) \
                        .decode('utf-8') \
                        .splitlines()[1:]
        for database in databases:
            self.backup_database(tmp_dir, database)

    def backup(self, out_file: str, tmp_dir: str):
        log.info("starting backup with mysqldump")
        if self._all_databases:
            self.backup_all_databases(tmp_dir)
        else:
            for database in self._databases:
                self.backup_database(tmp_dir, database)

        util.zipdir(out_file, tmp_dir)

    @classmethod
    def get_provider_key(cls) -> str:
        return "mysqldump"
