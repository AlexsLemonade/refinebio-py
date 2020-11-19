import unittest
import pyrefinebio

from unittest.mock import Mock, patch

from tests.custom_assertions import CustomAssertions
from tests.mocks import MockResponse


item0 = {
    "id": 1,
    "name": "test-1",
    "version": 1,
    "docker_image": "test-1",
    "environment": "test-1"
}

item1 = {
    "id": 2,
    "name": "test-2",
    "version": 1,
    "docker_image": "test-2",
    "environment": "test-2"
}

item2 = {
    "id": 3,
    "name": "test-3",
    "version": 1,
    "docker_image": "test-3",
    "environment": "test-3"
}

item3 = {
    "id": 4,
    "name": "test-4",
    "version": 1,
    "docker_image": "test-4",
    "environment": "test-4"
}

page1 = {
    "count": 4,
    "next": "search_2",
    "previous": None,
    "results": [item0, item1]
}

page2 = {
    "count": 4,
    "next": "search_2",
    "previous": None,
    "results": [item2, item3]
}

def mock_request(method, url, **kwargs):

    if url == "https://api.refine.bio/v1/test/" and not kwargs:
        return MockResponse(page1, url)

    if url == "https://api.refine.bio/v1/test/" and kwargs["params"] == {"offset": 2, "limit": 2}:
        return MockResponse(page2, url)
        

class DatasetTests(unittest.TestCase, CustomAssertions):

    def setUp(self):
        T = pyrefinebio.Processor
        response = MockResponse(page1, "https://api.refine.bio/v1/test/")
        self.paginatedList = pyrefinebio.util.create_paginated_list(T, response)


    @patch("pyrefinebio.http.requests.request", side_effect=mock_request)
    def test_indexing(self, mock_request):
        self.assertObject(self.paginatedList[0], item0)
        self.assertObject(self.paginatedList[1], item1)
        self.assertObject(self.paginatedList[2], item2)
        self.assertObject(self.paginatedList[3], item3)

        self.assertObject(self.paginatedList[-1], item3)
        self.assertObject(self.paginatedList[-2], item2)

        with self.assertRaises(IndexError):
            self.paginatedList[4]

        with self.assertRaises(IndexError):
            self.paginatedList[-5]


    @patch("pyrefinebio.http.requests.request", side_effect=mock_request)
    def test_iteration(self, mock_request):
        actual = [item0, item1, item2, item3]

        i = 0

        for processor in self.paginatedList:
            self.assertObject(processor, actual[i])
            i += 1
