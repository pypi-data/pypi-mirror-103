import base64

import paramiko

from backup_tool.providers.storage import StorageProvider
import pysftp
import backup_tool.util as util
import logging

log = logging.getLogger("SFTPStorageProvider")


def _get_cnops(key: str) -> pysftp.CnOpts:
    segments = key.split()
    cnops = pysftp.CnOpts()
    cnops.hostkeys.add(segments[0], segments[1], paramiko.RSAKey(data=base64.b64decode(segments[2])))
    return cnops


def _get_filename(backup_name: str, timestamp: int):
    return "{timestamp}_{name}".format(timestamp=timestamp, name=backup_name)


class SFTPStorageProvider(StorageProvider):

    def __init__(self, provider_config: dict):
        self._host = util.require_not_null(provider_config["host"], "host")
        self._username = util.require_not_null(provider_config["username"], "username")
        self._password = util.require_not_null(provider_config["password"], "password")
        self._host_key = util.require_not_null(provider_config["hostKey"], "hostKey")

        if "root" in provider_config:
            self._root = provider_config["root"]
        else:
            self._root = "/"

    def save(self, path: str, backup_name: str, timestamp: int):
        log.info("Saving backup file")
        with pysftp.Connection(self._host, username=self._username, password=self._password,
                               cnopts=_get_cnops(self._host_key)) as sftp:
            self._setup_workspace(sftp, backup_name)
            sftp.put(path, _get_filename(backup_name, timestamp))

    def delete(self, backup_name: str, timestamp: int):
        log.info("Deleting backup file")
        with pysftp.Connection(self._host, username=self._username, password=self._password,
                               cnopts=_get_cnops(self._host_key)) as sftp:
            self._setup_workspace(sftp, backup_name)
            if sftp.exists(_get_filename(backup_name, timestamp)):
                sftp.remove(_get_filename(backup_name, timestamp))

    def _setup_workspace(self, sftp, backup_name: str):
        sftp.chdir(self._root)
        if not sftp.exists(backup_name):
            sftp.mkdir(backup_name)
        sftp.chdir(backup_name)

    @classmethod
    def get_provider_key(cls) -> str:
        return "sftp"
