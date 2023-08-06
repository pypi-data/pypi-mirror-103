import json
from backup_tool.backup import Backup
import logging
import os


def ensure_config_exists():
    if not os.path.exists("config"):
        os.mkdir("config")
    if not os.path.exists("config/config.json"):
        with open("config/config.json", "x") as config_file:
            json.dump({"backups": []}, config_file, indent=4)


def load_config():
    ensure_config_exists()
    with open("config/config.json") as config_file:
        return json.load(config_file)


def main():
    logging.basicConfig(format='%(asctime)s %(levelname)s:%(name)s: %(message)s', level=logging.INFO)
    logging.info("Loading backup config...")
    config = load_config()
    for backup_config in config["backups"]:
        backup = Backup(backup_config, None)
        backup.run()
        print()


if __name__ == "__main__":
    main()
