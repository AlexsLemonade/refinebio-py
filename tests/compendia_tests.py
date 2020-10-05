import unittest
import pyrefinebio
from unittest.mock import Mock, patch

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

def mock_get_request(url, **kwargs):

    class MockResponse:
        def __init__(self, json_data):
            self.json_data = json_data

        def json(self):
            return self.json_data
        
        def raise_for_status(self):
            pass

    if url == "https://api.refine.bio/v1/compendia/1/":
        return MockResponse(compendia_object_1)

    if url == "https://api.refine.bio/v1/compendia/":
        return MockResponse(search_1)

    if url == "search_2":
        return MockResponse(search_2)

class CompendiaTests(unittest.TestCase):

    @patch("pyrefinebio.http.requests.get", side_effect=mock_get_request)
    def test_compendia_get(self, mock_get):
        result = pyrefinebio.Compendia.get(1)
        self.assertCompendia(result, compendia_object_1)

    @patch("pyrefinebio.http.requests.get", side_effect=mock_get_request)
    def test_compendia_search_no_filters(self, mock_get):
        result = pyrefinebio.Compendia.search()

        result_list = list(result)

        self.assertCompendia(result_list[0], compendia_object_1)
        self.assertCompendia(result_list[1], compendia_object_2)

        self.assertEqual(len(mock_get.call_args_list), 2)


    def assertCompendia(self, actual, expected):
        # Assert that feilds returned are properly set and can be accessed by dot notation
        self.assertEqual(actual.id, expected["id"])
        self.assertEqual(actual.primary_organism_name, expected["primary_organism_name"])
        self.assertListEqual(actual.organism_names, expected["organism_names"])
        self.assertEqual(actual.svd_algorithm, expected["svd_algorithm"])
        self.assertEqual(actual.quant_sf_only, expected["quant_sf_only"])
        self.assertEqual(actual.compendium_version, expected["compendium_version"])

        self.assertEqual(actual.computed_file.id, expected["computed_file"]["id"])
        self.assertEqual(actual.computed_file.filename, expected["computed_file"]["filename"])
        self.assertEqual(actual.computed_file.size_in_bytes, expected["computed_file"]["size_in_bytes"])
        self.assertEqual(actual.computed_file.is_smashable, expected["computed_file"]["is_smashable"])
        self.assertEqual(actual.computed_file.is_qc, expected["computed_file"]["is_qc"])
        self.assertEqual(actual.computed_file.sha1, expected["computed_file"]["sha1"])
        self.assertEqual(actual.computed_file.s3_bucket, expected["computed_file"]["s3_bucket"])
        self.assertEqual(actual.computed_file.s3_key, expected["computed_file"]["s3_key"])
        self.assertEqual(actual.computed_file.created_at, expected["computed_file"]["created_at"])
        self.assertEqual(actual.computed_file.last_modified, expected["computed_file"]["last_modified"])

        # Assert that non-returned feilds are set to their default values
        self.assertIsNone(actual.computed_file.compendia_organism_name)
        self.assertIsNone(actual.computed_file.compendia_version)
        self.assertIsNone(actual.computed_file.download_url)
        self.assertIsNone(actual.computed_file.quant_sf_only)
        self.assertIsNone(actual.computed_file.result)
        self.assertIsNone(actual.computed_file.s3_url)
        self.assertListEqual(actual.computed_file.samples, [])

