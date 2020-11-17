import logging
import os
from pathlib import Path

import yaml
from pyrefinebio.http import get_by_endpoint, post_by_endpoint, put_by_endpoint
from pyrefinebio.config import Config


class Token:
    """Handles the creation, activation, saving, and loading of api tokens.

    These tokens can be used in requests that provide urls to download computed files.

    Please review refine.bio's [Terms of Use](https://www.refine.bio/terms) and [Privacy Policy](https://www.refine.bio/privacy)
    before use of these tokens.
    """

    @classmethod
    def create_token(cls, email_address):
        """creates a token and emails the terms and conditions to a specified email.

        parameters:

            email_address (str): the email that the terms and conditions should be sent to.
        """

        response = post_by_endpoint("token").json()

        token_id = response["id"]

        if email_address:
            terms = response["terms_and_conditions"]
            # email terms

        return token_id

    @classmethod
    def agree_to_terms_and_conditions(cls, api_token):
        """Activates a token.

        Activating a token indicates agreement with refine.bio's
        [Terms of Use](https://www.refine.bio/terms) and
        [Privacy Policy](https://www.refine.bio/privacy).

        parameters:

            api_token (str): the uuid string identifying the token
                             you want to activate.
        """
        return put_by_endpoint("token/" + api_token, payload={"is_activated": True})

    @classmethod
    def save_token(cls, api_token):
        """Saves a token to the config file.

        The default config file is ~/.refinebio.yaml, but
        you can use the environment variable `CONFIG_FILE` to change this path

        parameters:

            api_token (str): the uuid string identifying the token
                             you want to save.
        """
        config = Config()
        config.save("token", api_token)

    @classmethod
    def get_token(cls):
        """gets the token that's currently saved to the config file.

        The default config file is ~/.refinebio.yaml, but
        you can use the environment variable `CONFIG_FILE` to change this path
        """
        config = Config()
        return config.token
