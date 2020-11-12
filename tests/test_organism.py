import unittest
import pyrefinebio
from unittest.mock import Mock, patch

from tests.custom_assertions import CustomAssertions
from tests.mocks import MockResponse


gorilla = {
    "name": "GORILLA",
    "taxonomy_id": 9592
}

mouse = {
    "name": "MUS",
    "taxonomy_id": 862507
}

search_1 = {
    "count": 2,
    "next": "search_2",
    "previous": None,
    "results": [gorilla]
}

search_2 = {
    "count": 2,
    "next": None,
    "previous": "search_1",
    "results": [mouse]
}

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

    @patch("pyrefinebio.http.requests.request", side_effect=mock_request)
    def test_organism_get(self, mock_request):
        result = pyrefinebio.Organism.get("GORILLA")
        self.assertObject(result, gorilla)


    @patch("pyrefinebio.http.requests.request", side_effect=mock_request)
    def test_organism_500(self, mock_request):
        with self.assertRaises(Exception):
            pyrefinebio.Organism.get(500)


    @patch("pyrefinebio.http.requests.request", side_effect=mock_request)
    def test_organism_get_404(self, mock_request):
        with self.assertRaises(Exception):
            pyrefinebio.Organism.get("HUMAN")


    @patch("pyrefinebio.http.requests.request", side_effect=mock_request)
    def test_organism_search_no_filters(self, mock_request):
        result = pyrefinebio.Organism.search()

        result_list = list(result)

        self.assertObject(result_list[0], gorilla)
        self.assertObject(result_list[1], mouse)

        self.assertEqual(len(mock_request.call_args_list), 2)
