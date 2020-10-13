import unittest
import pyrefinebio
from unittest.mock import Mock, patch

from .custom_assertions import CustomAssertions

computational_result_1 = {
    "id": 0,
    "commands": [
        "test1",
        "test2"
    ],
    "processor": {
        "id": 0,
        "name": "test_processor",
        "version": "1",
        "docker_image": "test_image",
        "environment": {}
    },
    "is_ccdl": True,
    "annotations": [
        {
            "id": 0,
            "data": "annotation",
            "is_ccdl": True,
            "created_at": "2020-10-02T18:48:24Z",
            "last_modified": "2020-10-02T18:48:24Z"
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
            "last_modified": "2020-10-02T18:48:24Z"
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
        "last_modified": "2020-10-02T18:48:24Z"
    },
    "time_start": "2020-10-02T18:48:24Z",
    "time_end": "2020-10-02T18:48:24Z",
    "created_at": "2020-10-02T18:48:24Z",
    "last_modified": "2020-10-02T18:48:24Z"
}

computational_result_2 = {
    "id": 0,
    "commands": [
        "test1",
        "test2"
    ],
    "processor": {
        "id": 0,
        "name": "test_processor",
        "version": "1",
        "docker_image": "test_image",
        "environment": {}
    },
    "is_ccdl": True,
    "annotations": [
        {
            "id": 0,
            "data": "annotation",
            "is_ccdl": True,
            "created_at": "2020-10-02T18:48:24Z",
            "last_modified": "2020-10-02T18:48:24Z"
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
            "last_modified": "2020-10-02T18:48:24Z"
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
        "last_modified": "2020-10-02T18:48:24Z"
    },
    "time_start": "2020-10-02T18:48:24Z",
    "time_end": "2020-10-02T18:48:24Z",
    "created_at": "2020-10-02T18:48:24Z",
    "last_modified": "2020-10-02T18:48:24Z"
}

search_1 = {
    "count": 2,
    "next": "search_2",
    "previous": None,
    "results": [computational_result_1]
}

search_2 = {
    "count": 2,
    "next": None,
    "previous": "search_1",
    "results": [computational_result_2]
}

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

    if url == "https://api.refine.bio/v1/computational_results/1/":
        return MockResponse(computational_result_1)

    if url == "https://api.refine.bio/v1/computational_results/0/":
        return MockResponse(None, status=404)

    if url == "https://api.refine.bio/v1/computational_results/500/":
        return MockResponse(None, status=500)

    if url == "https://api.refine.bio/v1/computational_results/":
        return MockResponse(search_1)

    if url == "search_2":
        return MockResponse(search_2)

class ComputationalResultTests(unittest.TestCase, CustomAssertions):

    @patch("pyrefinebio.http.requests.request", side_effect=mock_request)
    def test_computational_result_get(self, mock_request):
        result = pyrefinebio.ComputationalResult.get(1)
        self.assertObject(result, computational_result_1)


    @patch("pyrefinebio.http.requests.request", side_effect=mock_request)
    def test_computational_result_500(self, mock_request):
        with self.assertRaises(Exception):
            pyrefinebio.ComputationalResult.get(500)


    @patch("pyrefinebio.http.requests.request", side_effect=mock_request)
    def test_computational_result_get_404(self, mock_request):
        with self.assertRaises(Exception):
            pyrefinebio.ComputationalResult.get(0)


    @patch("pyrefinebio.http.requests.request", side_effect=mock_request)
    def test_computational_result_search_no_filters(self, mock_request):
        result = pyrefinebio.ComputationalResult.search()

        result_list = list(result)

        self.assertObject(result_list[0], computational_result_1)
        self.assertObject(result_list[1], computational_result_2)

        self.assertEqual(len(mock_request.call_args_list), 2)


    def test_computational_result_search_with_filters(self):
        pass


    def test_computational_result_search_with_invalid_filters(self):
        with self.assertRaises(Exception):
            pyrefinebio.ComputationalResult.search(foo="bar")
