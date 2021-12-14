import unittest
from unittest.mock import Mock, patch

import pyrefinebio
from tests.custom_assertions import CustomAssertions
from tests.mocks import MockResponse

gorilla = {
    "name": "GORILLA",
    "taxonomy_id": 9592,
    "has_compendia": True,
    "has_quantfile_compendia": False,
}

mouse = {
    "name": "MUS",
    "taxonomy_id": 862507,
    "has_compendia": False,
    "has_quantfile_compendia": True,
}

search_1 = {"count": 2, "next": "search_2", "previous": None, "results": [gorilla]}

search_2 = {"count": 2, "next": None, "previous": "search_1", "results": [mouse]}


def mock_request(method, url, **kwargs):

    if url == "https://api.refine.bio/v1/organisms/GORILLA/":
        return MockResponse(gorilla, url)

    if url == "https://api.refine.bio/v1/organisms/HUMAN/":
        return MockResponse(None, url, status=404)

    if url == "https://api.refine.bio/v1/organisms/500/":
        return MockResponse(None, url, status=500)

    if url == "https://api.refine.bio/v1/organisms/":
        return MockResponse(search_1, "search_2")

    if url == "search_2":
        return MockResponse(search_2, url)


class OrganismTests(unittest.TestCase, CustomAssertions):
    @patch("pyrefinebio.api_interface.requests.request", side_effect=mock_request)
    def test_organism_get(self, mock_request):
        result = pyrefinebio.Organism.get("GORILLA")
        self.assertObject(result, gorilla)

    @patch("pyrefinebio.api_interface.requests.request", side_effect=mock_request)
    def test_organism_500(self, mock_request):
        with self.assertRaises(Exception):
            pyrefinebio.Organism.get(500)

    @patch("pyrefinebio.api_interface.requests.request", side_effect=mock_request)
    def test_organism_get_404(self, mock_request):
        with self.assertRaises(Exception):
            pyrefinebio.Organism.get("HUMAN")

    @patch("pyrefinebio.api_interface.requests.request", side_effect=mock_request)
    def test_organism_search_no_filters(self, mock_request):
        results = pyrefinebio.Organism.search()

        self.assertObject(results[0], gorilla)
        self.assertObject(results[1], mouse)

    def test_organism_search_with_filters(self):
        filtered_results = pyrefinebio.Organism.search(has_quantfile_compendia=True)

        for result in filtered_results:
            self.assertTrue(result.has_quantfile_compendia)

    def test_organism_search_with_invalid_filters(self):
        with self.assertRaises(pyrefinebio.exceptions.InvalidFilters):
            pyrefinebio.OriginalFile.search(foo="bar")
