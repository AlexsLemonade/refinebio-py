import os
from pathlib import Path

import yaml


class Config:
    """Config for pyrefinebio.

    When instantiated, configurations are pulled first from environment variables,  
    then from the config file locaed at `~/.refinebio.yaml`. If neither exist, default  
    values are used.
    """

    _instance = None

    def __new__(cls):
        """Create an instance of config

        config attributes are loaded from environment variables first, then the config file  
        at `~/.refinebio.yaml`, then defaults
        
        returns: Config
        """
        if not cls._instance:
            cls._instance = super(Config, cls).__new__(cls)

            cls.config_file = (
                os.getenv("CONFIG_FILE") or str(Path.home()) + "/.refinebio.yaml"
            )

            config = {}

            if os.path.exists(cls.config_file):
                with open(cls.config_file) as config_file:
                    config = yaml.full_load(config_file) or {}

            cls.token = config.get("token", "")
            cls.base_url = os.getenv("BASE_URL") or config.get("base_url") or "https://api.refine.bio/v1/"

        return cls._instance

    def save(self, key, value):
        """Save a value to the config

        Values that are saved are written to the config file.  
        The default path for this file is `~/.refinebio.yaml`  
        but it can be set using the environment variable `CONFIG_FILE`.
        """
        if not os.path.exists(self.config_file):
            config = {}
        else:
            with open(self.config_file, "r") as config_file:
                config = yaml.full_load(config_file) or {}

        config[key] = value
        setattr(self._instance, key, value)

        with open(self.config_file, "w") as config_file:
            yaml.dump(config, config_file)
