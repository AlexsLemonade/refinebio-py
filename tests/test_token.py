import unittest
import pyrefinebio
import os
from unittest.mock import Mock, mock_open, patch

from .custom_assertions import CustomAssertions
from .mocks import MockResponse


token = {
    "id": "123456789",
    "is_activated": False,
    "terms_and_conditions": "TL;DR"
}

def mock_request(method, url, **kwargs):

    if url == "https://api.refine.bio/v1/token/":
        return MockResponse(token, url)


class TokenTests(unittest.TestCase, CustomAssertions):

    @classmethod
    def tearDownClass(cls):
        if os.path.exists("./temp"):
            os.remove("./temp")

    @patch("pyrefinebio.http.requests.request", side_effect=mock_request)
    def test_token_create(self, mock_request):
        result = pyrefinebio.Token.create_token("")
        self.assertEqual(result, token["id"])
        mock_request.assert_called_with("POST", "https://api.refine.bio/v1/token/", params=None, data=None)

    @patch("pyrefinebio.token.yaml.dump")
    @patch("pyrefinebio.token.open")
    def test_token_save(self, mock_open, mock_yaml):
        mock_open.return_value.__enter__.return_value = "file"

        pyrefinebio.Token.save_token("123456789", "test")

        mock_open.assert_called_with("test", "w")
        mock_yaml.assert_called_with({"token": "123456789"}, "file")


    def test_token_save_creates_file(self):
        if os.path.exists("./temp"):
            os.remove("./temp")

        self.assertFalse(os.path.exists("./temp"))

        pyrefinebio.Token.save_token("123456789", "./temp")

        self.assertTrue(os.path.exists("./temp"))


    @patch("pyrefinebio.token.os.path.exists")
    @patch("pyrefinebio.token.yaml.full_load")
    @patch("pyrefinebio.token.open")
    def test_token_load(self, mock_open, mock_load, mock_exists):
        mock_exists.return_value = True
        mock_load.return_value = {"token": "123456789"}

        token = pyrefinebio.Token.load_token("test")

        mock_open.assert_called_with("test")
        self.assertEqual(token, "123456789")

    def test_token_load_bad_file(self):
        with self.assertRaises(Exception):
            token = pyrefinebio.Token.load_token("bad_file")
