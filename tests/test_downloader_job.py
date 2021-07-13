import unittest
from copy import deepcopy
from unittest.mock import patch

import pyrefinebio
from pyrefinebio import original_file as prb_original_file
from tests.custom_assertions import CustomAssertions
from tests.mocks import MockResponse

job_1 = {
    "id": 1,
    "downloader_task": "SRA",
    "num_retries": 0,
    "retried": False,
    "was_recreated": True,
    "worker_id": "i-013f4473d78ce5cef",
    "worker_version": "v1.39.3-dev-hotfix",
    "batch_job_id": "faf15c0e-3164-4bae-98f6-c6668f9ff4a5",
    "batch_job_queue": "data-refinery-batch-workers-queue-circleci-prod-0",
    "failure_reason": None,
    "success": True,
    "original_files": [412392, 412403],
    "start_time": "2020-09-29T21:34:43.735081Z",
    "end_time": "2020-09-29T21:34:57.725233Z",
    "created_at": "2020-07-01T16:47:18.384967Z",
    "last_modified": "2020-09-29T21:34:57.725247Z",
}

job_2 = {
    "id": 2,
    "downloader_task": "SRA",
    "num_retries": 2,
    "retried": True,
    "was_recreated": False,
    "worker_id": "i-097213f99819c2edc",
    "worker_version": "v1.36.9-dev-hotfix",
    "batch_job_id": "2d4174c9-c449-49c5-b9c2-f270ec4597f0",
    "batch_job_queue": "data-refinery-batch-workers-queue-circleci-prod-0",
    "failure_reason": "Exception caught while downloading file\\n [Errno 28] No space left on device",
    "success": False,
    "original_files": [396995],
    "start_time": "2020-06-25T09:56:06.692840Z",
    "end_time": "2020-06-25T10:07:55.920347Z",
    "created_at": "2020-06-25T09:56:04.731805Z",
    "last_modified": "2020-06-25T10:07:56.601791Z",
}

job_1_object_dict = deepcopy(job_1)

job_1_object_dict["original_files"] = [
    prb_original_file.OriginalFile(file_id) for file_id in job_1["original_files"]
]

job_2_object_dict = deepcopy(job_2)

job_2_object_dict["original_files"] = [
    prb_original_file.OriginalFile(file_id) for file_id in job_2["original_files"]
]

search_1 = {"count": 2, "next": "search_2", "previous": None, "results": [job_1]}

search_2 = {"count": 2, "next": None, "previous": "search_1", "results": [job_2]}


def mock_request(method, url, **kwargs):

    if url == "https://api.refine.bio/v1/jobs/downloader/1/":
        return MockResponse(job_1, url)

    if url == "https://api.refine.bio/v1/jobs/downloader/2/":
        return MockResponse(job_2, url)

    if url == "https://api.refine.bio/v1/jobs/downloader/0/":
        return MockResponse(None, url, status=404)

    if url == "https://api.refine.bio/v1/jobs/downloader/500/":
        return MockResponse(None, url, status=500)

    if url == "https://api.refine.bio/v1/jobs/downloader/":
        return MockResponse(search_1, "search_2")

    if url == "search_2":
        return MockResponse(search_2, url)


class DownloaderJobTests(unittest.TestCase, CustomAssertions):
    @patch("pyrefinebio.api_interface.requests.request", side_effect=mock_request)
    def test_downloader_job_get(self, mock_request):
        result = pyrefinebio.DownloaderJob.get(1)
        self.assertObject(result, job_1_object_dict)

    @patch("pyrefinebio.api_interface.requests.request", side_effect=mock_request)
    def test_downloader_job_500(self, mock_request):
        with self.assertRaises(pyrefinebio.exceptions.ServerError):
            pyrefinebio.DownloaderJob.get(500)

    @patch("pyrefinebio.api_interface.requests.request", side_effect=mock_request)
    def test_downloader_job_get_404(self, mock_request):
        with self.assertRaises(pyrefinebio.exceptions.NotFound):
            pyrefinebio.DownloaderJob.get(0)

    @patch("pyrefinebio.api_interface.requests.request", side_effect=mock_request)
    def test_downloader_job_search_no_filters(self, mock_request):
        results = pyrefinebio.DownloaderJob.search()

        self.assertObject(results[0], job_1_object_dict)
        self.assertObject(results[1], job_2_object_dict)

    def test_downloader_job_search_with_filters(self):
        filtered_results = pyrefinebio.DownloaderJob.search(
            success=True, retried=True, num_retries=1, downloader_task="GEO"
        )

        for result in filtered_results:
            self.assertTrue(result.success)
            self.assertTrue(result.retried)
            self.assertEqual(result.num_retries, 1)
            self.assertEqual(result.downloader_task, "GEO")

    def test_downloader_job_search_with_invalid_filters(self):
        with self.assertRaises(pyrefinebio.exceptions.InvalidFilters):
            pyrefinebio.DownloaderJob.search(foo="bar")
