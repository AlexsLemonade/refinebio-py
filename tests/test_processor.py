import unittest
from unittest.mock import Mock, patch

import pyrefinebio
from tests.custom_assertions import CustomAssertions
from tests.mocks import MockResponse

processor_1 = {
    "id": 1,
    "name": "test processor 1",
    "version": "v1.0.1",
    "docker_image": "test_image_1",
    "environment": {
        "os_pkg": {
            "g++": "4:5.3.1-1ubuntu1",
            "python3": "3.5.1-3",
            "python3-pip": "8.1.1-2ubuntu0.4",
        },
        "python": {"Django": "2.0.6", "data-refinery-common": "1.0.1"},
        "cmd_line": {
            "salmon --version": "salmon 0.9.1",
            "rsem-calculate-expression --version": "Current version: RSEM v1.3.1",
        },
        "os_distribution": "Ubuntu 16.04.5 LTS",
    },
}

processor_2 = {
    "id": 2,
    "name": "test processor 2",
    "version": "v1.0.1",
    "docker_image": "test_image_2",
    "environment": {
        "os_pkg": {"python3": "3.5.1-3", "python3-pip": "8.1.1-2ubuntu0.4"},
        "python": {"Django": "2.0.6", "data-refinery-common": "1.0.1"},
        "cmd_line": {"fasterq-dump --version": "fasterq-dump : 2.9.1"},
        "os_distribution": "Ubuntu 16.04.5 LTS",
    },
}

search_1 = {"count": 2, "next": "search_2", "previous": None, "results": [processor_1]}

search_2 = {"count": 2, "next": None, "previous": "search_1", "results": [processor_2]}


def mock_request(method, url, **kwargs):

    if url == "https://api.refine.bio/v1/processors/1/":
        return MockResponse(processor_1, url)

    if url == "https://api.refine.bio/v1/processors/0/":
        return MockResponse(None, url, status=404)

    if url == "https://api.refine.bio/v1/processors/500/":
        return MockResponse(None, url, status=500)

    if url == "https://api.refine.bio/v1/processors/":
        return MockResponse(search_1, "search_2")

    if url == "search_2":
        return MockResponse(search_2, url)


class ProcessorTests(unittest.TestCase, CustomAssertions):
    @patch("pyrefinebio.api_interface.requests.request", side_effect=mock_request)
    def test_processor_get(self, mock_request):
        result = pyrefinebio.Processor.get(1)
        self.assertObject(result, processor_1)

    @patch("pyrefinebio.api_interface.requests.request", side_effect=mock_request)
    def test_processor_500(self, mock_request):
        with self.assertRaises(Exception):
            pyrefinebio.Processor.get(500)

    @patch("pyrefinebio.api_interface.requests.request", side_effect=mock_request)
    def test_processor_get_404(self, mock_request):
        with self.assertRaises(Exception):
            pyrefinebio.Processor.get(0)

    @patch("pyrefinebio.api_interface.requests.request", side_effect=mock_request)
    def test_processor_search_no_filters(self, mock_request):
        results = pyrefinebio.Processor.search()

        self.assertObject(results[0], processor_1)
        self.assertObject(results[1], processor_2)
