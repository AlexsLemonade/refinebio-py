import unittest
import pyrefinebio
from unittest.mock import Mock, patch

from tests.custom_assertions import CustomAssertions
from tests.mocks import MockResponse


job_1 = {
    "id": 1,
    "pipeline_applied": "JANITOR",
    "num_retries": 0,
    "retried": False,
    "worker_id": None,
    "ram_amount": 2048,
    "volume_index": "-1",
    "worker_version": None,
    "failure_reason": None,
    "nomad_job_id": None,
    "success": None,
    "original_files": [],
    "datasets": [],
    "start_time": None,
    "end_time": None,
    "created_at": "2020-10-14T17:30:09.480064Z",
    "last_modified": "2020-10-14T17:30:09.493173Z"
}

job_2 = {
    "id": 2,
    "pipeline_applied": "SMASHER",
    "num_retries": 0,
    "retried": False,
    "worker_id": "i-01877387b773bc7b4",
    "ram_amount": 4096,
    "volume_index": None,
    "worker_version": "v1.39.11",
    "failure_reason": None,
    "nomad_job_id": "SMASHER/dispatch-1602694804-d9a3164b",
    "success": True,
    "original_files": [
        12345,
        13456,
        14567
    ],
    "datasets": [
        "test-set-1",
        "test-set-2"
    ],
    "start_time": "2020-10-14T17:00:38.579600Z",
    "end_time": "2020-10-14T17:02:12.439331Z",
    "created_at": "2020-10-14T17:00:04.154755Z",
    "last_modified": "2020-10-14T17:02:12.658330Z"
}

search_1 = {
    "count": 2,
    "next": "search_2",
    "previous": None,
    "results": [job_1]
}

search_2 = {
    "count": 2,
    "next": None,
    "previous": "search_1",
    "results": [job_2]
}

def mock_request(method, url, **kwargs):

    if url == "https://api.refine.bio/v1/jobs/processor/1/":
        return MockResponse(job_1, url)

    if url == "https://api.refine.bio/v1/jobs/processor/0/":
        return MockResponse(None, url, status=404)

    if url == "https://api.refine.bio/v1/jobs/processor/500/":
        return MockResponse(None, url, status=500)

    if url == "https://api.refine.bio/v1/jobs/processor/":
        return MockResponse(search_1, "search_2")

    if url == "search_2":
        return MockResponse(search_2, url)

class ProcessorJobTests(unittest.TestCase, CustomAssertions):

    @patch("pyrefinebio.http.requests.request", side_effect=mock_request)
    def test_processor_job_get(self, mock_request):
        result = pyrefinebio.ProcessorJob.get(1)
        self.assertObject(result, job_1)


    @patch("pyrefinebio.http.requests.request", side_effect=mock_request)
    def test_processor_job_500(self, mock_request):
        with self.assertRaises(pyrefinebio.exceptions.ServerError):
            pyrefinebio.ProcessorJob.get(500)


    @patch("pyrefinebio.http.requests.request", side_effect=mock_request)
    def test_processor_job_get_404(self, mock_request):
        with self.assertRaises(pyrefinebio.exceptions.NotFound):
            pyrefinebio.ProcessorJob.get(0)


    @patch("pyrefinebio.http.requests.request", side_effect=mock_request)
    def test_processor_job_search_no_filters(self, mock_request):
        result = pyrefinebio.ProcessorJob.search()

        result_list = list(result)

        self.assertObject(result_list[0], job_1)
        self.assertObject(result_list[1], job_2)

        self.assertEqual(len(mock_request.call_args_list), 2)


    def test_processor_job_search_with_filters(self):
        filtered_results = pyrefinebio.ProcessorJob.search(retried=True, num_retries=4, pipeline_applied="QN_REFERENCE")

        for result in filtered_results:
            self.assertTrue(result.retried)
            self.assertEqual(result.num_retries, 4)
            self.assertEqual(result.pipeline_applied, "QN_REFERENCE")


    def test_processor_job_search_with_invalid_filters(self):
        with self.assertRaises(pyrefinebio.exceptions.InvalidFilters):
            pyrefinebio.ProcessorJob.search(foo="bar")
