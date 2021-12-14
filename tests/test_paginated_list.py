import unittest
from unittest.mock import Mock, patch

import pyrefinebio
from tests.custom_assertions import CustomAssertions
from tests.mocks import MockResponse

item0 = {"id": 1, "name": "test-1", "version": 1, "docker_image": "test-1", "environment": "test-1"}

item1 = {"id": 2, "name": "test-2", "version": 1, "docker_image": "test-2", "environment": "test-2"}

item2 = {"id": 3, "name": "test-3", "version": 1, "docker_image": "test-3", "environment": "test-3"}

item3 = {"id": 4, "name": "test-4", "version": 1, "docker_image": "test-4", "environment": "test-4"}

page1 = {"count": 4, "next": "search_2", "previous": None, "results": [item0, item1]}

page2 = {"count": 4, "next": "search_2", "previous": None, "results": [item2, item3]}


def processor(id):
    return {
        "id": id,
        "name": "test-4",
        "version": 1,
        "docker_image": "test-4",
        "environment": "test-4",
    }


def mock_request(method, url, **kwargs):

    if url == "https://api.refine.bio/v1/test/" and not kwargs:
        return MockResponse(page1, url)

    if url == "https://api.refine.bio/v1/test/" and kwargs["params"] == {"offset": 2, "limit": 2}:
        return MockResponse(page2, url)

    if url == "https://api.refine.bio/v1/processors/" and kwargs["params"] == {"limit": 10}:
        return MockResponse(
            {
                "count": 20,
                "next": "foo",
                "previous": None,
                "results": [processor(i) for i in range(10)],
            },
            url,
        )

    if url == "https://api.refine.bio/v1/processors/" and kwargs["params"] == {
        "offset": 10,
        "limit": 10,
    }:
        return MockResponse(
            {
                "count": 20,
                "next": "foo",
                "previous": None,
                "results": [processor(i) for i in range(10, 20)],
            },
            url,
        )


class PaginatedListTests(unittest.TestCase, CustomAssertions):
    @patch("pyrefinebio.api_interface.requests.request", side_effect=mock_request)
    def test_indexing(self, mock_request):
        T = pyrefinebio.Processor
        response = MockResponse(page1, "https://api.refine.bio/v1/test/")
        paginatedList = pyrefinebio.util.create_paginated_list(T, response)

        self.assertObject(paginatedList[0], item0)
        self.assertObject(paginatedList[1], item1)
        self.assertObject(paginatedList[2], item2)
        self.assertObject(paginatedList[3], item3)

        self.assertObject(paginatedList[-1], item3)
        self.assertObject(paginatedList[-2], item2)

        with self.assertRaises(IndexError):
            paginatedList[4]

        with self.assertRaises(IndexError):
            paginatedList[-5]

    @patch("pyrefinebio.api_interface.requests.request", side_effect=mock_request)
    def test_iteration(self, mock_request):
        T = pyrefinebio.Processor
        response = MockResponse(page1, "https://api.refine.bio/v1/test/")
        paginatedList = pyrefinebio.util.create_paginated_list(T, response)

        actual = [item0, item1, item2, item3]

        i = 0

        for processor in paginatedList:
            self.assertObject(processor, actual[i])
            i += 1

    @patch("pyrefinebio.api_interface.requests.request", side_effect=mock_request)
    def test_slicing(self, mock_request):
        paginatedList = pyrefinebio.Processor.search(limit=10)

        actual = paginatedList[5:15]

        self.assertEqual(len(actual), 10)

        self.assertObject(actual[0], processor(5))
        self.assertObject(actual[1], processor(6))
        self.assertObject(actual[2], processor(7))
        self.assertObject(actual[3], processor(8))
        self.assertObject(actual[4], processor(9))
        self.assertObject(actual[5], processor(10))
        self.assertObject(actual[6], processor(11))
        self.assertObject(actual[7], processor(12))
        self.assertObject(actual[8], processor(13))
        self.assertObject(actual[9], processor(14))

        self.assertEqual(len(mock_request.call_args_list), 2)

    @patch("pyrefinebio.api_interface.requests.request", side_effect=mock_request)
    def test_slicing_with_step(self, mock_request):
        paginatedList = pyrefinebio.Processor.search(limit=10)

        actual = paginatedList[5:15:2]

        self.assertEqual(len(actual), 5)

        self.assertObject(actual[0], processor(5))
        self.assertObject(actual[1], processor(7))
        self.assertObject(actual[2], processor(9))
        self.assertObject(actual[3], processor(11))
        self.assertObject(actual[4], processor(13))

        self.assertEqual(len(mock_request.call_args_list), 2)

    @patch("pyrefinebio.api_interface.requests.request", side_effect=mock_request)
    def test_slicing_negative_indices(self, mock_request):
        paginatedList = pyrefinebio.Processor.search(limit=10)

        actual = paginatedList[5:-5]

        self.assertEqual(len(actual), 10)

        self.assertObject(actual[0], processor(5))
        self.assertObject(actual[1], processor(6))
        self.assertObject(actual[2], processor(7))
        self.assertObject(actual[3], processor(8))
        self.assertObject(actual[4], processor(9))
        self.assertObject(actual[5], processor(10))
        self.assertObject(actual[6], processor(11))
        self.assertObject(actual[7], processor(12))
        self.assertObject(actual[8], processor(13))
        self.assertObject(actual[9], processor(14))

        self.assertEqual(len(mock_request.call_args_list), 2)

    @patch("pyrefinebio.api_interface.requests.request", side_effect=mock_request)
    def test_slicing_negative_step(self, mock_request):
        paginatedList = pyrefinebio.Processor.search(limit=10)

        actual = paginatedList[15:5:-1]

        self.assertEqual(len(actual), 10)

        self.assertObject(actual[0], processor(15))
        self.assertObject(actual[1], processor(14))
        self.assertObject(actual[2], processor(13))
        self.assertObject(actual[3], processor(12))
        self.assertObject(actual[4], processor(11))
        self.assertObject(actual[5], processor(10))
        self.assertObject(actual[6], processor(9))
        self.assertObject(actual[7], processor(8))
        self.assertObject(actual[8], processor(7))
        self.assertObject(actual[9], processor(6))

        self.assertEqual(len(mock_request.call_args_list), 2)

    @patch("pyrefinebio.api_interface.requests.request", side_effect=mock_request)
    def test_slicing_default_start_stop(self, mock_request):
        paginatedList = pyrefinebio.Processor.search(limit=10)

        actual = paginatedList[::5]

        self.assertEqual(len(actual), 4)

        self.assertObject(actual[0], processor(0))
        self.assertObject(actual[1], processor(5))
        self.assertObject(actual[2], processor(10))
        self.assertObject(actual[3], processor(15))

    @patch("pyrefinebio.api_interface.requests.request", side_effect=mock_request)
    def test_slicing_default_start_stop_negative_step(self, mock_request):
        paginatedList = pyrefinebio.Processor.search(limit=10)

        actual = paginatedList[::-5]

        self.assertEqual(len(actual), 4)

        self.assertObject(actual[0], processor(19))
        self.assertObject(actual[1], processor(14))
        self.assertObject(actual[2], processor(9))
        self.assertObject(actual[3], processor(4))
