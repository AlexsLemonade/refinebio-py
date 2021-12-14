import unittest
from unittest.mock import patch

import pyrefinebio
from pyrefinebio.exceptions import BadRequest, NotFound
from tests.custom_assertions import CustomAssertions
from tests.mocks import MockResponse


def mock_400_request(method, url, **kwargs):
    return MockResponse(
        "we're not home right now", "https://api.refine.bio/v1/organisms/GORILLA", 400
    )


def mock_404_request(method, url, **kwargs):
    return MockResponse(
        "we're not home right now", "https://api.refine.bio/v1/organisms/GORILLA", 404
    )


class ApiInterfaceTests(unittest.TestCase, CustomAssertions):
    @patch("pyrefinebio.api_interface.requests.request", side_effect=mock_400_request)
    def test_400(self, mock_request):
        with self.assertRaises(BadRequest):
            pyrefinebio.Organism.get("GORILLA")

    @patch("pyrefinebio.api_interface.requests.request", side_effect=mock_404_request)
    def test_404(self, mock_request):
        with self.assertRaises(NotFound):
            pyrefinebio.Organism.get("GORILLA")
