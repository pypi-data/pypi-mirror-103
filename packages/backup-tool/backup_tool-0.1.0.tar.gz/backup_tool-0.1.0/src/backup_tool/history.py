import backup_tool.util as util
import json
from shutil import copyfile
import os


def ensure_history_exists(path: str):
    if not os.path.exists("backups"):
        os.mkdir("backups")
    if not os.path.exists(path):
        with open(path, "x") as history_file:
            json.dump([], history_file)


class BackupInstance:

    def __init__(self, timestamp, size):
        self.timestamp = util.require_not_null(timestamp, "timestamp")
        self.size = util.require_not_null(size, "size")

    def to_dict(self):
        return {
            "timestamp": self.timestamp,
            "size": self.size
        }


class History:
    HISTORY_FILE_LOCATION = "backups/{backup_name}.json"
    HISTORY_BACKUP_FILE_LOCATION = "backups/{backup_name}.json.old"

    def __init__(self, backup_name: str):
        self.backup_name = backup_name
        ensure_history_exists(self.HISTORY_FILE_LOCATION.format(backup_name=self.backup_name))

        with open(self.HISTORY_FILE_LOCATION.format(backup_name=self.backup_name)) as history_file:
            self._current_backups = json.load(history_file)

    def _save(self):
        copyfile(self.HISTORY_FILE_LOCATION.format(backup_name=self.backup_name),
                 self.HISTORY_BACKUP_FILE_LOCATION.format(backup_name=self.backup_name))
        with open(self.HISTORY_FILE_LOCATION.format(backup_name=self.backup_name), "w") as history_file:
            json.dump(self._current_backups, history_file, indent=4)

    def is_empty(self):
        return len(self._current_backups) == 0

    def get_newest_backup(self) -> BackupInstance:
        backup = self._current_backups[-1]
        return BackupInstance(backup["timestamp"], backup["size"])

    def get_oldest_backup(self) -> BackupInstance:
        backup = self._current_backups[0]
        return BackupInstance(backup["timestamp"], backup["size"])

    def push_back(self, instance: BackupInstance):
        self._current_backups.append(instance.to_dict())
        self._save()

    def remove_last(self):
        self._current_backups.pop(0)
        self._save()
