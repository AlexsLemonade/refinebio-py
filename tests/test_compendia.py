import unittest
import pyrefinebio
from unittest.mock import Mock, patch

from .custom_assertions import CustomAssertions
from .mocks import MockResponse


compendia_object_1 = {
    "id": 69,
    "primary_organism_name": "HUMAN",
    "organism_names": [
        "HUMAN",
        "GORILLA"
    ],
    "svd_algorithm": "NONE",
    "quant_sf_only": True,
    "compendium_version": 1,
    "computed_file": {
        "id": 420,
        "filename": "test-compendia.zip",
        "size_in_bytes": 5000,
        "is_smashable": False,
        "is_qc": False,
        "sha1": "3c5de2dba42c2768e7542a0262d2b9a1e9fc9f45",
        "s3_bucket": "test-bucket",
        "s3_key": "test-compendia.zip",
        "created_at": "2020-10-02:00:00.0Z",
        "last_modified": "2020-10-02:00:00.0Z"
    }
}

compendia_object_2 = {
    "id": 42,
    "primary_organism_name": "GORILLA",
    "organism_names": [
        "HUMAN",
        "GORILLA"
    ],
    "svd_algorithm": "NONE",
    "quant_sf_only": True,
    "compendium_version": 1,
    "computed_file": {
        "id": 4,
        "filename": "test-compendia-2.zip",
        "size_in_bytes": 7500,
        "is_smashable": True,
        "is_qc": False,
        "sha1": "3c5de2dba42c2768e7542a0262d2b9a1e9fc9f45",
        "s3_bucket": "test-bucket",
        "s3_key": "test-compendia-2.zip",
        "created_at": "2020-10-05:00:00.0Z",
        "last_modified": "2020-10-05:00:00.0Z"
    }
}

search_1 = {
    "count": 2,
    "next": "search_2",
    "previous": None,
    "results": [compendia_object_1]
}

search_2 = {
    "count": 2,
    "next": None,
    "previous": "search_1",
    "results": [compendia_object_2]
}

def mock_request(method, url, **kwargs):

    if url == "https://api.refine.bio/v1/compendia/1/":
        return MockResponse(compendia_object_1, url)

    if url == "https://api.refine.bio/v1/compendia/0/":
        return MockResponse(None, url, status=404)

    if url == "https://api.refine.bio/v1/compendia/500/":
        return MockResponse(None, url, status=500)

    if url == "https://api.refine.bio/v1/compendia/":
        return MockResponse(search_1, url)

    if url == "search_2":
        return MockResponse(search_2, url)

class CompendiaTests(unittest.TestCase, CustomAssertions):

    @patch("pyrefinebio.http.requests.request", side_effect=mock_request)
    def test_compendia_get(self, mock_request):
        result = pyrefinebio.Compendia.get(1)
        self.assertObject(result, compendia_object_1)


    @patch("pyrefinebio.http.requests.request", side_effect=mock_request)
    def test_compendia_500(self, mock_request):
        with self.assertRaises(pyrefinebio.exceptions.ServerError):
            pyrefinebio.Compendia.get(500)


    @patch("pyrefinebio.http.requests.request", side_effect=mock_request)
    def test_compendia_get_404(self, mock_request):
        with self.assertRaises(pyrefinebio.exceptions.NotFound):
            pyrefinebio.Compendia.get(0)


    @patch("pyrefinebio.http.requests.request", side_effect=mock_request)
    def test_compendia_search_no_filters(self, mock_request):
        result = pyrefinebio.Compendia.search()

        result_list = list(result)

        self.assertObject(result_list[0], compendia_object_1)
        self.assertObject(result_list[1], compendia_object_2)

        self.assertEqual(len(mock_request.call_args_list), 2)


    def test_compendia_search_with_filters(self):
        non_filtered_results = pyrefinebio.Compendia.search()
        filtered_results = pyrefinebio.Compendia.search(primary_organism__name="ACTINIDIA_CHINENSIS")

        self.assertTrue(len(list(filtered_results)) < len(list(non_filtered_results)))


    def test_compendia_search_with_invalid_filters(self):
        with self.assertRaises(pyrefinebio.exceptions.InvalidFilters):
            pyrefinebio.Compendia.search(foo="bar")
