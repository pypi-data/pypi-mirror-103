from abc import ABC, abstractmethod

import backup_tool.providers as providers
import backup_tool.util as util


class Transformer(providers.Provider, ABC):

    @abstractmethod
    def transform(self, input_path: str, output_path: str):
        pass


def get_transformer(transformer_config: dict) -> Transformer:
    from backup_tool.providers.transformer.AESEncryptionTransformer import AESEncryptionTransformer

    provider_key = util.require_not_null(transformer_config["type"], "type")
    if provider_key == AESEncryptionTransformer.get_provider_key():
        return AESEncryptionTransformer(transformer_config)

    raise ValueError("Transformer with name '{name}' does not exist".format(name=provider_key))
