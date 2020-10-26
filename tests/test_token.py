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
        result = pyrefinebio.Token.create_token("")
        self.assertEqual(result, token["id"])


    @patch("pyrefinebio.config.yaml.dump")
    @patch("pyrefinebio.config.open")
    def test_token_save(self, mock_open, mock_yaml):
        os.environ["CONFIG_FILE"] = "test"
        mock_open.return_value.__enter__.return_value = "file"

        pyrefinebio.Token.save_token("123456789")

        mock_open.assert_called_with("test", "w")
        mock_yaml.assert_called_with({"token": "123456789"}, "file")


    def test_token_save_creates_file(self):
        os.environ["CONFIG_FILE"] = "./temp"

        if os.path.exists("./temp"):
            os.remove("./temp")

        pyrefinebio.Token.save_token("123456789")

        self.assertTrue(os.path.exists("./temp"))


    @patch("pyrefinebio.config.os.path.exists")
    @patch("pyrefinebio.config.yaml.full_load")
    @patch("pyrefinebio.config.open")
    def test_token_get(self, mock_open, mock_load, mock_exists):
        os.environ["CONFIG_FILE"] = "./temp"
        mock_open.return_value.__enter__.return_value = "file"
        mock_load.return_value = {"token": "this-is-a-test-token"}
        mock_exists.return_value = True

        token = pyrefinebio.Token.get_token()

        self.assertEqual(token, "this-is-a-test-token")
