import unittest
import pyrefinebio
from unittest.mock import Mock, patch

from .custom_assertions import CustomAssertions


platforms = [
    {
        "platform_accession_code": "testcode1",
        "platform_name": "test platform 1"
    },
    {
        "platform_accession_code": "testcode2",
        "platform_name": "test platform 2"
    },
    {
        "platform_accession_code": "testcode3",
        "platform_name": "test platform 3"
    },
    {
        "platform_accession_code": "testcode4",
        "platform_name": "test platform 4"
    },
]


def mock_request(method, url, **kwargs):

    class MockResponse:
        def __init__(self, json_data, status=200):
            self.json_data = json_data
            self.status = status

        def json(self):
            return self.json_data
        
        def raise_for_status(self):
            if self.status != 200:
                raise Exception

    if url == "https://api.refine.bio/v1/platforms/":
        return MockResponse(platforms)


class PlatfromTest(unittest.TestCase, CustomAssertions):

    @patch("pyrefinebio.http.requests.request", side_effect=mock_request)
    def test_computed_file_get(self, mock_request):
        result = pyrefinebio.Platform.search()

        self.assertEqual(len(result), len(platforms))

        for i in range(len(result)):
            self.assertObject(result[i], platforms[i])
