# WIP
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

            if not os.path.exists(cls.config_file):
                with open(cls.config_file, 'w'): pass


            with open(cls.config_file) as config_file:
                config = yaml.full_load(config_file)
                cls.token = config["token"] or ""

        return cls._instance
