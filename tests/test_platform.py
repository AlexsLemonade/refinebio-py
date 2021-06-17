import unittest
from unittest.mock import Mock, patch

import pyrefinebio
from tests.custom_assertions import CustomAssertions
from tests.mocks import MockResponse

platforms = [
    {"platform_accession_code": "testcode1", "platform_name": "test platform 1"},
    {"platform_accession_code": "testcode2", "platform_name": "test platform 2"},
    {"platform_accession_code": "testcode3", "platform_name": "test platform 3"},
    {"platform_accession_code": "testcode4", "platform_name": "test platform 4"},
]


def mock_request(method, url, **kwargs):

    if url == "https://api.refine.bio/v1/platforms/":
        return MockResponse(platforms, url)


class PlatfromTest(unittest.TestCase, CustomAssertions):
    @patch("pyrefinebio.api_interface.requests.request", side_effect=mock_request)
    def test_computed_file_get(self, mock_request):
        result = pyrefinebio.Platform.search()

        self.assertEqual(len(result), len(platforms))

        for i in range(len(result)):
            self.assertObject(result[i], platforms[i])
