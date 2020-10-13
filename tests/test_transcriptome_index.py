import unittest
import pyrefinebio
from unittest.mock import Mock, patch

from .custom_assertions import CustomAssertions


index_1 = {
    "id": 1,
    "assembly_name": "0",
    "organism_name": "CYPRINUS_CARPIO",
    "database_name": "EnsemblMain",
    "release_version": "101",
    "index_type": "TRANSCRIPTOME_SHORT",
    "salmon_version": "salmon 0.13.1",
    "download_url": "test-url",
    "result_id": 2784457,
    "last_modified": "2020-10-01T19:11:44.029922Z"
}

index_2 = {
    "id": 2,
    "assembly_name": "0",
    "organism_name": "HUMAN",
    "database_name": "EnsemblMain",
    "release_version": "101",
    "index_type": "TRANSCRIPTOME_LONG",
    "salmon_version": "salmon 0.13.1",
    "download_url": "test-url",
    "result_id": 2784456,
    "last_modified": "2020-10-01T19:11:06.836302Z"
}

search_1 = {
    "count": 2,
    "next": "search_2",
    "previous": None,
    "results": [index_1]
}

search_2 = {
    "count": 2,
    "next": None,
    "previous": "search_1",
    "results": [index_2]
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

    if url == "https://api.refine.bio/v1/transcriptome_indices/1/":
        return MockResponse(index_1)

    if url == "https://api.refine.bio/v1/transcriptome_indices/0/":
        return MockResponse(None, status=404)

    if url == "https://api.refine.bio/v1/transcriptome_indices/500/":
        return MockResponse(None, status=500)

    if url == "https://api.refine.bio/v1/transcriptome_indices/":
        return MockResponse(search_1)

    if url == "search_2":
        return MockResponse(search_2)


class TranscriptomeIndexTests(unittest.TestCase, CustomAssertions):

    @patch("pyrefinebio.http.requests.request", side_effect=mock_request)
    def test_transcriptome_index_get(self, mock_request):
        result = pyrefinebio.TranscriptomeIndex.get(1)
        self.assertObject(result, index_1)


    @patch("pyrefinebio.http.requests.request", side_effect=mock_request)
    def test_transcriptome_index_500(self, mock_request):
        with self.assertRaises(Exception):
            pyrefinebio.TranscriptomeIndex.get(500)


    @patch("pyrefinebio.http.requests.request", side_effect=mock_request)
    def test_transcriptome_index_404(self, mock_request):
        with self.assertRaises(Exception):
            pyrefinebio.TranscriptomeIndex.get(0)


    @patch("pyrefinebio.http.requests.request", side_effect=mock_request)
    def test_transcriptome_index_search_no_filters(self, mock_request):
        result = pyrefinebio.TranscriptomeIndex.search()

        result_list = list(result)

        self.assertObject(result_list[0], index_1)
        self.assertObject(result_list[1], index_2)

        self.assertEqual(len(mock_request.call_args_list), 2)
