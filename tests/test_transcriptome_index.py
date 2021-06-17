import unittest
from unittest.mock import Mock, patch

import pyrefinebio
from tests.custom_assertions import CustomAssertions
from tests.mocks import MockResponse

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
    "last_modified": "2020-10-01T19:11:44.029922Z",
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
    "last_modified": "2020-10-01T19:11:06.836302Z",
}

search_1 = {"count": 2, "next": "search_2", "previous": None, "results": [index_1]}

search_2 = {"count": 2, "next": None, "previous": "search_1", "results": [index_2]}


def mock_request(method, url, **kwargs):

    if url == "https://api.refine.bio/v1/transcriptome_indices/1/":
        return MockResponse(index_1, url)

    if url == "https://api.refine.bio/v1/transcriptome_indices/0/":
        return MockResponse(None, url, status=404)

    if url == "https://api.refine.bio/v1/transcriptome_indices/500/":
        return MockResponse(None, url, status=500)

    if url == "https://api.refine.bio/v1/transcriptome_indices/":
        return MockResponse(search_1, "search_2")

    if url == "search_2":
        return MockResponse(search_2, url)


class TranscriptomeIndexTests(unittest.TestCase, CustomAssertions):
    @patch("pyrefinebio.api_interface.requests.request", side_effect=mock_request)
    def test_transcriptome_index_get(self, mock_request):
        result = pyrefinebio.TranscriptomeIndex.get(1)
        self.assertObject(result, index_1)

    @patch("pyrefinebio.api_interface.requests.request", side_effect=mock_request)
    def test_transcriptome_index_500(self, mock_request):
        with self.assertRaises(Exception):
            pyrefinebio.TranscriptomeIndex.get(500)

    @patch("pyrefinebio.api_interface.requests.request", side_effect=mock_request)
    def test_transcriptome_index_404(self, mock_request):
        with self.assertRaises(Exception):
            pyrefinebio.TranscriptomeIndex.get(0)

    @patch("pyrefinebio.api_interface.requests.request", side_effect=mock_request)
    def test_transcriptome_index_search_no_filters(self, mock_request):
        results = pyrefinebio.TranscriptomeIndex.search()

        self.assertObject(results[0], index_1)
        self.assertObject(results[1], index_2)

    def test_transcriptome_index_search_with_filters(self):
        filtered_results = pyrefinebio.TranscriptomeIndex.search(
            index_type="TRANSCRIPTOME_SHORT",
            salmon_version="salmon 0.13.1",
            organism__name="CYPRINUS_CARPIO",
        )

        for result in filtered_results:
            self.assertEqual(result.index_type, "TRANSCRIPTOME_SHORT")
            self.assertEqual(result.salmon_version, "salmon 0.13.1")
            self.assertEqual(result.organism_name, "CYPRINUS_CARPIO")
