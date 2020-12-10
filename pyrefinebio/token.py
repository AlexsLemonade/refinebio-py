import logging
import os
from pathlib import Path

import yaml
from pyrefinebio.http import get_by_endpoint, post_by_endpoint, put_by_endpoint
from pyrefinebio.config import Config
from pyrefinebio.exceptions import NotFound, BadRequest


class Token:
    """Handles the creation, activation, saving, and loading of api tokens.

    These tokens can be used in requests that provide urls to download computed files.

    Please review refine.bio's [Terms of Use](https://www.refine.bio/terms) and [Privacy Policy](https://www.refine.bio/privacy)
    before use of these tokens.

    Create a new Token

        >>> import pyrefinebio
        >>> token = pyrefinebio.Token(email_address="foo@bar.com")

    Create a Token and activate it

        >>> import pyrefinebio
        >>> token = pyrefinebio.Token(email_address="foo@bar.com")
        >>> token.agree_to_terms_and_conditions()

    Save a Token to the config file

        >>> import pyrefinebio
        >>> token = pyrefinebio.Token(email_address="foo@bar.com")
        >>> token.save_token()

    Load the Token that is currently saved to the config file

        >>> import pyrefinebio
        >>> token = pyrefinebio.Token.load_token()
    """

    def __init__(
        self,
        email_address=None,
        id=None,
    ):
        if id:
            try:
                response = get_by_endpoint("token/" + str(id)).json()
            except NotFound:
                raise BadRequest(
                    "Token with id '" + str(id) + "' does not exist in RefineBio. " 
                    "Please create a new token."
                )
        else:
            response = post_by_endpoint(
                "token",
                payload={
                    "email_address": email_address
                }
            ).json()

        self.email_address = email_address

        self.token_id = response["id"]
        self.is_activated = response["is_activated"]
        self.terms_and_conditions = response["terms_and_conditions"]


    def agree_to_terms_and_conditions(self):
        """Activates a token.

        Activating a token indicates agreement with refine.bio's
        [Terms of Use](https://www.refine.bio/terms) and
        [Privacy Policy](https://www.refine.bio/privacy).
        """
        return put_by_endpoint("token/" + self.token_id, payload={"is_activated": True})


    def save_token(self):
        """Saves a token to the config file.

        The default config file is ~/.refinebio.yaml, but
        you can use the environment variable `CONFIG_FILE` to change this path
        """
        config = Config()
        config.save("token", self.token_id)


    @classmethod
    def get_token(cls):
        """gets the token that's currently saved to the config file.

        The default config file is ~/.refinebio.yaml, but
        you can use the environment variable `CONFIG_FILE` to change this path
        """
        config = Config()
        return Token(id=config.token)

    def __str__(self):
        return str(self.token_id)
