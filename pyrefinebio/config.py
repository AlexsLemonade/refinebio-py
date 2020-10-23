import os
from pathlib import Path

import yaml


class Config:

    _instance = None

    def __new__(cls):
        if not cls._instance:
            cls._instance = super(Config, cls).__new__(cls)

            cls.config_file = (
                os.getenv("CONFIG_FILE") or str(Path.home()) + "/.refinebio.yaml"
            )

            config = {}

            if os.path.exists(cls.config_file):
                with open(cls.config_file) as config_file:
                    config = yaml.full_load(config_file) or {}

            cls.token = config.get("token") or ""
            cls.base_url = os.getenv("BASE_URL") or config.get("base_url") or "https://api.refine.bio/v1/"

        return cls._instance

    def save(self, key, value):
        if not os.path.exists(self.config_file):
            with open(self.config_file, 'w'): pass

        config = {}

        with open(self.config_file, "r") as config_file:
            config = yaml.full_load(config_file) or {}

        config[key] = value
        setattr(self._instance, key, value)

        with open(self.config_file, "w") as config_file:
            yaml.dump(config, config_file)
