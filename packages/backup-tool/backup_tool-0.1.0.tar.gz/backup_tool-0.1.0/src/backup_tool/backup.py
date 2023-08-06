import datetime

import backup_tool.util as util
from backup_tool.history import History, BackupInstance
import backup_tool.interval as interval
import backup_tool.providers.backup as backup
import backup_tool.providers.storage as storage
import backup_tool.providers.transformer as transformer
import tempfile
import os
import time
import logging
from datetime import datetime

log = logging.getLogger("backup")


class Backup:
    WORKSPACE = "workspace"
    BACKUP_FILE_NAME = ""

    def __init__(self, backup_config: dict, provider_config: dict):
        self.name = util.require_not_null(backup_config["name"], "name")
        self.interval = interval.parse_interval(util.require_not_null(backup_config["interval"], "interval"))
        self.keep = interval.parse_interval(util.require_not_null(backup_config["keep"], "keep"))
        self.backup_provider = backup.get_backup_provider(util.require_not_null(backup_config["backup"], "backup"))
        self.storage_provider = storage.get_storage_provider(util.require_not_null(backup_config["storage"], "storage"))
        self.history = History(self.name)

        if "transformers" in backup_config:
            self.transformers = map(lambda config: transformer.get_transformer(config), backup_config["transformers"])
        else:
            self.transformers = []

    def should_create(self, timestamp: int):
        if self.history.is_empty():
            return True
        next_backup = self.history.get_newest_backup().timestamp + self.interval
        log.info("Next backup {name} scheduled at {date}".format(name=self.name,
                                                                 date=str(datetime.fromtimestamp(next_backup / 1000))))
        return next_backup < timestamp

    def delete_old(self, timestamp):
        def try_delete_next() -> bool:
            if self.history.is_empty():
                return False
            next_backup = self.history.get_oldest_backup()
            delete_at = next_backup.timestamp + self.keep
            log.info("Next backup {name} scheduled for deletion at {date}".format(name=self.name, date=str(
                datetime.fromtimestamp(delete_at / 1000))))
            if delete_at < timestamp:
                log.info("Deleting...")
                self.storage_provider.delete(self.name, next_backup.timestamp)
                self.history.remove_last()
                return True
            return False

        while try_delete_next():
            pass

    def create_new(self, timestamp):
        log.info("Creating new backup {name}".format(name=self.name))
        if not os.path.exists(self.WORKSPACE):
            os.mkdir(self.WORKSPACE)
        root = tempfile.TemporaryDirectory(dir=self.WORKSPACE)
        os.mkdir(os.path.join(root.name, "backupWorkspace"))
        output_file = os.path.join(root.name, "backup.out")
        self.backup_provider.backup(output_file, os.path.join(root.name, "backupWorkspace"))

        final_file = output_file
        for i, trans in enumerate(self.transformers):
            next_file = output_file + str(i)
            trans.transform(final_file, next_file)
            final_file = next_file

        self.history.push_back(BackupInstance(timestamp, os.path.getsize(output_file)))

        self.storage_provider.save(final_file, self.name, timestamp)
        root.cleanup()

    def run(self):
        log.info("Running {name}".format(name=self.name))
        timestamp = int(time.time() * 1000)
        self.delete_old(timestamp)
        if self.should_create(timestamp):
            self.create_new(timestamp)
