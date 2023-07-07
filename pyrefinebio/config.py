import os
from pathlib import Path

import yaml


class Config:
    """Config for pyrefinebio.

    Config values can be set by environment variables or in the Config file.

    The Config file's default location is `~/.refinebio.yaml`, but this location
    can be set by using the environment variable `REFINEBIO_CONFIG_FILE`

    pyrefinebio's configurable values are:

        token:
            The refine.bio API token that is used when making requests

            environment variable: `REFINEBIO_TOKEN`

        base_url:
            The base url for the refine.bio API that should be used
            when making requests. The default is `https://api.refine.bio/v1/`

            environment variable: `REFINEBIO_BASE_URL`

        api_max_calls_per_second:
            The refine.bio API calls per second limit. This defaults to the API's rate limit
            which is enforced per IP address.

            environment variable: `REFINEBIO_API_MAX_CALLS_PER_SECOND`

    These config values can be modified directly in code, but it recommended that you
    set them by using environment variables, by modifying them in Config file, or by
    using other class methods provided - like `pyrefinebio.Token` for example.

    example Config file:

    .. code-block:: shell

        token: foo-bar-baz
        base_url: https://api.refine.bio/v1/
        api_max_calls_per_second: 10
    """

    _instance = None

    def __new__(cls):
        """Create an instance of config

        Config values are loaded from environment variables first, then the config file,
        then they are set to defaults.

        returns:
            Config
        """
        if not cls._instance:
            cls._instance = super(Config, cls).__new__(cls)

            cls.config_file = (
                os.getenv("REFINEBIO_CONFIG_FILE") or str(Path.home()) + "/.refinebio.yaml"
            )

            config = {}

            if os.path.exists(cls.config_file):
                with open(cls.config_file) as config_file:
                    config = yaml.safe_load(config_file) or {}

            cls.token = os.getenv("REFINEBIO_TOKEN") or config.get("token", "")
            cls.base_url = os.getenv("REFINEBIO_BASE_URL") or config.get(
                "base_url", "https://api.refine.bio/v1/"
            )
            cls.api_max_calls_per_second = int(
                os.getenv("REFINEBIO_API_MAX_CALLS_PER_SECOND")
                or config.get("api_max_calls_per_second", 10)
            )

        return cls._instance

    def save(self):
        """Save the config to a file

        The default path for this file is `~/.refinebio.yaml`
        but it can be set using the environment variable `REFINEBIO_CONFIG_FILE`.
        """
        config = {
            "token": self.token,
            "base_url": self.base_url,
            "api_max_calls_per_second": self.api_max_calls_per_second,
        }

        with open(self.config_file, "w") as config_file:
            yaml.dump(config, config_file)
