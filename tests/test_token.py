import unittest
import pyrefinebio
from pyrefinebio.config import Config
import os
from unittest.mock import Mock, mock_open, patch
from importlib import reload

from tests.custom_assertions import CustomAssertions
from tests.mocks import MockResponse


token = {
    "id": "123456789",
    "is_activated": False,
    "terms_and_conditions": "TL;DR"
}

def mock_request(method, url, **kwargs):

    if url == "https://api.refine.bio/v1/token/":
        return MockResponse(token, url)

    if url == "https://api.refine.bio/v1/token/123456789/":
        return MockResponse(token, url)


class TokenTests(unittest.TestCase, CustomAssertions):

    def setUp(self):
        Config._instance = None

    @classmethod
    def tearDownClass(cls):
        if os.path.exists("./temp"):
            os.remove("./temp")
        
        os.environ.pop("CONFIG_FILE", None)


    @patch("pyrefinebio.http.requests.request", side_effect=mock_request)
    def test_token_create(self, mock_request):
        result = pyrefinebio.Token(email_address="")
        self.assertEqual(result.token_id, token["id"])


    @patch("pyrefinebio.config.yaml.dump")
    @patch("pyrefinebio.config.open")
    @patch("pyrefinebio.http.requests.request", side_effect=mock_request)
    def test_token_save(self, mock_request, mock_open, mock_yaml):
        os.environ["CONFIG_FILE"] = "test"
        mock_open.return_value.__enter__.return_value = "file"

        token = pyrefinebio.Token()
        token.save_token()

        mock_open.assert_called_with("test", "w")
        mock_yaml.assert_called_with({"token": token.token_id}, "file")


    @patch("pyrefinebio.http.requests.request", side_effect=mock_request)
    def test_token_save_creates_file(self, mock_request):
        os.environ["CONFIG_FILE"] = "./temp"

        if os.path.exists("./temp"):
            os.remove("./temp")

        token = pyrefinebio.Token()
        token.save_token()

        self.assertTrue(os.path.exists("./temp"))


    def test_token_save_bad_id(self):
        with self.assertRaises(pyrefinebio.exceptions.BadRequest) as br:
            token = pyrefinebio.Token(id="test")
            token.save_token()

        self.assertEqual(
            br.exception.base_message,
            "Bad Request: "
            "Token with id 'test' does not exist in RefineBio. " 
            "Please create a new token."
        )



    @patch("pyrefinebio.http.requests.request", side_effect=mock_request)
    def test_token_save_unactivated(self, mock_request):
        with self.assertRaises(pyrefinebio.exceptions.BadRequest) as br:
            token = pyrefinebio.Token(id="123456789")
            token.save_token()

        self.assertEqual(
            br.exception.base_message,
            "Bad Request: "
            "Token with id '123456789' is not activated. " 
            "Please activate your token with `agree_to_terms_and_conditions()` before saving it."
        )


    @patch("pyrefinebio.token.get_by_endpoint")
    @patch("pyrefinebio.config.os.path.exists")
    @patch("pyrefinebio.config.yaml.full_load")
    @patch("pyrefinebio.config.open")
    def test_token_get(self, mock_open, mock_load, mock_exists, mock_get):
        os.environ["CONFIG_FILE"] = "./temp"
        mock_open.return_value.__enter__.return_value = "file"
        mock_load.return_value = {"token": "this-is-a-test-token"}
        mock_exists.return_value = True

        token = pyrefinebio.Token.get_token()

        self.assertEqual(token.id, "this-is-a-test-token")

