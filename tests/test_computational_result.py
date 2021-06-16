import unittest
from unittest.mock import Mock, patch

import pyrefinebio
from tests.custom_assertions import CustomAssertions
from tests.mocks import MockResponse

computational_result_1 = {
    "id": 1,
    "commands": ["test1", "test2"],
    "processor": {
        "id": 0,
        "name": "test_processor",
        "version": "1",
        "docker_image": "test_image",
        "environment": {},
    },
    "is_ccdl": True,
    "annotations": [
        {
            "id": 0,
            "data": "annotation",
            "is_ccdl": True,
            "created_at": "2020-10-02T18:48:24Z",
            "last_modified": "2020-10-02T18:48:24Z",
        }
    ],
    "files": [
        {
            "id": 0,
            "filename": "string",
            "size_in_bytes": -9223372036854776000,
            "is_smashable": True,
            "is_qc": True,
            "sha1": "string",
            "s3_bucket": "string",
            "s3_key": "string",
            "created_at": "2020-10-02T18:48:24Z",
            "last_modified": "2020-10-02T18:48:24Z",
        }
    ],
    "organism_index": {
        "id": 0,
        "assembly_name": "string",
        "organism_name": "string",
        "database_name": "string",
        "release_version": "string",
        "index_type": "string",
        "salmon_version": "string",
        "download_url": "string",
        "result_id": "string",
        "last_modified": "2020-10-02T18:48:24Z",
    },
    "time_start": "2020-10-02T18:48:24Z",
    "time_end": "2020-10-02T18:48:24Z",
    "created_at": "2020-10-02T18:48:24Z",
    "last_modified": "2020-10-02T18:48:24Z",
}

computational_result_2 = {
    "id": 2,
    "commands": ["test1", "test2"],
    "processor": {
        "id": 0,
        "name": "test_processor",
        "version": "1",
        "docker_image": "test_image",
        "environment": {},
    },
    "is_ccdl": True,
    "annotations": [
        {
            "id": 0,
            "data": "annotation",
            "is_ccdl": True,
            "created_at": "2020-10-02T18:48:24Z",
            "last_modified": "2020-10-02T18:48:24Z",
        }
    ],
    "files": [
        {
            "id": 0,
            "filename": "string",
            "size_in_bytes": -9223372036854776000,
            "is_smashable": True,
            "is_qc": True,
            "sha1": "string",
            "s3_bucket": "string",
            "s3_key": "string",
            "created_at": "2020-10-02T18:48:24Z",
            "last_modified": "2020-10-02T18:48:24Z",
        }
    ],
    "organism_index": {
        "id": 0,
        "assembly_name": "string",
        "organism_name": "string",
        "database_name": "string",
        "release_version": "string",
        "index_type": "string",
        "salmon_version": "string",
        "download_url": "string",
        "result_id": "string",
        "last_modified": "2020-10-02T18:48:24Z",
    },
    "time_start": "2020-10-02T18:48:24Z",
    "time_end": "2020-10-02T18:48:24Z",
    "created_at": "2020-10-02T18:48:24Z",
    "last_modified": "2020-10-02T18:48:24Z",
}

search_1 = {"count": 2, "next": "search_2", "previous": None, "results": [computational_result_1]}

search_2 = {"count": 2, "next": None, "previous": "search_1", "results": [computational_result_2]}


def mock_request(method, url, **kwargs):

    if url == "https://api.refine.bio/v1/computational_results/1/":
        return MockResponse(computational_result_1, url)

    if url == "https://api.refine.bio/v1/computational_results/2/":
        return MockResponse(computational_result_2, url)

    if url == "https://api.refine.bio/v1/computational_results/0/":
        return MockResponse(None, url, status=404)

    if url == "https://api.refine.bio/v1/computational_results/500/":
        return MockResponse(None, url, status=500)

    if url == "https://api.refine.bio/v1/computational_results/":
        return MockResponse(search_1, "search_2")

    if url == "search_2":
        return MockResponse(search_2, url)


class ComputationalResultTests(unittest.TestCase, CustomAssertions):
    @patch("pyrefinebio.api_interface.requests.request", side_effect=mock_request)
    def test_computational_result_get(self, mock_request):
        result = pyrefinebio.ComputationalResult.get(1)
        self.assertObject(result, computational_result_1)

    @patch("pyrefinebio.api_interface.requests.request", side_effect=mock_request)
    def test_computational_result_500(self, mock_request):
        with self.assertRaises(pyrefinebio.exceptions.ServerError):
            pyrefinebio.ComputationalResult.get(500)

    @patch("pyrefinebio.api_interface.requests.request", side_effect=mock_request)
    def test_computational_result_get_404(self, mock_request):
        with self.assertRaises(pyrefinebio.exceptions.NotFound):
            pyrefinebio.ComputationalResult.get(0)

    @patch("pyrefinebio.api_interface.requests.request", side_effect=mock_request)
    def test_computational_result_search_no_filters(self, mock_request):
        results = pyrefinebio.ComputationalResult.search()

        self.assertObject(results[0], computational_result_1)
        self.assertObject(results[1], computational_result_2)

    def test_computational_result_search_with_filters(self):
        filtered_results = pyrefinebio.ComputationalResult.search(processor__id=12)

        for result in filtered_results:
            self.assertEqual(result.processor.id, 12)

    def test_computational_result_search_with_invalid_filters(self):
        with self.assertRaises(pyrefinebio.exceptions.InvalidFilters):
            pyrefinebio.ComputationalResult.search(foo="bar")
