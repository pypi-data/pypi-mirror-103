from abc import ABC, abstractmethod
import backup_tool.providers as providers
import backup_tool.util as util


class BackupProvider(providers.Provider, ABC):

    @abstractmethod
    def backup(self, out_file: str, tmp_dir: str):
        pass


def get_backup_provider(provider_config: dict) -> BackupProvider:
    from backup_tool.providers.backup.MysqldumpBackupProvider import MysqldumpBackupProvider
    from backup_tool.providers.backup.PostgresqlBackupProvider import PostgresqlBackupProvider

    provider_key = util.require_not_null(provider_config["type"], "type")
    if provider_key == MysqldumpBackupProvider.get_provider_key():
        return MysqldumpBackupProvider(provider_config)
    if provider_key == PostgresqlBackupProvider.get_provider_key():
        return PostgresqlBackupProvider(provider_config)

    raise ValueError("Unsupported backup provider {name}".format(name=provider_key))
