import unittest
import pyrefinebio
from unittest.mock import Mock, patch

from tests.custom_assertions import CustomAssertions
from tests.mocks import MockResponse


compendium_object_1 = {
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
        "filename": "test-compendium.zip",
        "size_in_bytes": 5000,
        "is_smashable": False,
        "is_qc": False,
        "sha1": "3c5de2dba42c2768e7542a0262d2b9a1e9fc9f45",
        "s3_bucket": "test-bucket",
        "s3_key": "test-compendium.zip",
        "created_at": "2020-10-02T00:00:00Z",
        "last_modified": "2020-10-02T00:00:00Z"
    }
}

compendium_object_2 = {
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
        "filename": "test-compendium-2.zip",
        "size_in_bytes": 7500,
        "is_smashable": True,
        "is_qc": False,
        "sha1": "3c5de2dba42c2768e7542a0262d2b9a1e9fc9f45",
        "s3_bucket": "test-bucket",
        "s3_key": "test-compendium-2.zip",
        "created_at": "2020-10-05T00:00:00Z",
        "last_modified": "2020-10-05T00:00:00Z"
    }
}

search_1 = {
    "count": 2,
    "next": "search_2",
    "previous": None,
    "results": [compendium_object_1]
}

search_2 = {
    "count": 2,
    "next": None,
    "previous": "search_1",
    "results": [compendium_object_2]
}

def mock_request(method, url, **kwargs):

    if url == "https://api.refine.bio/v1/compendia/1/":
        return MockResponse(compendium_object_1, url)

    if url == "https://api.refine.bio/v1/compendia/0/":
        return MockResponse(None, url, status=404)

    if url == "https://api.refine.bio/v1/compendia/500/":
        return MockResponse(None, url, status=500)

    if url == "https://api.refine.bio/v1/compendia/":
        return MockResponse(search_1, "search_2")

    if url == "search_2":
        return MockResponse(search_2, url)

class CompendiumTests(unittest.TestCase, CustomAssertions):

    @patch("pyrefinebio.http.requests.request", side_effect=mock_request)
    def test_compendium_get(self, mock_request):
        result = pyrefinebio.Compendium.get(1)
        self.assertObject(result, compendium_object_1)


    @patch("pyrefinebio.http.requests.request", side_effect=mock_request)
    def test_compendium_500(self, mock_request):
        with self.assertRaises(pyrefinebio.exceptions.ServerError):
            pyrefinebio.Compendium.get(500)


    @patch("pyrefinebio.http.requests.request", side_effect=mock_request)
    def test_compendium_get_404(self, mock_request):
        with self.assertRaises(pyrefinebio.exceptions.NotFound):
            pyrefinebio.Compendium.get(0)


    @patch("pyrefinebio.http.requests.request", side_effect=mock_request)
    def test_compendium_search_no_filters(self, mock_request):
        results = pyrefinebio.Compendium.search()

        self.assertObject(results[0], compendium_object_1)
        self.assertObject(results[1], compendium_object_2)

        self.assertEqual(len(mock_request.call_args_list), 2)


    def test_compendium_search_with_filters(self):
        filtered_results = pyrefinebio.Compendium.search(primary_organism__name="ACTINIDIA_CHINENSIS")

        for result in filtered_results:
            self.assertEqual(result.primary_organism_name, "ACTINIDIA_CHINENSIS")


    def test_compendium_search_with_invalid_filters(self):
        with self.assertRaises(pyrefinebio.exceptions.InvalidFilters):
            pyrefinebio.Compendium.search(foo="bar")
