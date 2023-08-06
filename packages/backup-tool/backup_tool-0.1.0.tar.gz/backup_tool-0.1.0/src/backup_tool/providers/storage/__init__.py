from abc import ABC, abstractmethod

import backup_tool.providers as providers
import backup_tool.util as util


class StorageProvider(providers.Provider, ABC):
    @abstractmethod
    def save(self, path: str, backup_name: str, timestamp: int):
        pass

    @abstractmethod
    def delete(self, backup_name: str, timestamp: int):
        pass


def get_storage_provider(provider_config: dict) -> StorageProvider:
    from backup_tool.providers.storage.SFTPStorageProvider import SFTPStorageProvider

    provider_key = util.require_not_null(provider_config["type"], "type")
    if provider_key == SFTPStorageProvider.get_provider_key():
        return SFTPStorageProvider(provider_config)

    raise ValueError("Storage Provider with name '{name}' does not exist".format(name=provider_key))
