import backup_tool.util as util
from backup_tool.providers.transformer import Transformer
from subprocess import run
import logging

log = logging.getLogger("MysqldumpBackupProvider")


class AESEncryptionTransformer(Transformer):

    def __init__(self, config: dict):
        self._password = util.require_not_null(config["password"], "password")

    def transform(self, input_path: str, output_path: str):
        log.info("Encrypting backup file...")
        process = run(
            ["gpg", "-o", output_path, "--cipher-algo", "AES256", "--symmetric", "--batch", "--yes", "--passphrase-fd",
             "0", input_path],
            input=bytes(self._password, 'utf-8'))

        if process.returncode != 0:
            raise ChildProcessError("GPG returned status {status}".format(status=str(process.returncode)))

    @classmethod
    def get_provider_key(cls) -> str:
        return "aesEncryption"
