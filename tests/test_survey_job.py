import unittest
from unittest.mock import Mock, patch

import pyrefinebio
from tests.custom_assertions import CustomAssertions
from tests.mocks import MockResponse

job_1 = {
    "id": 1,
    "source_type": "GEO",
    "success": True,
    "start_time": "2020-10-13T14:38:02.287672Z",
    "end_time": "2020-10-13T14:50:52.962129Z",
    "created_at": "2020-10-13T14:38:02.275537Z",
    "last_modified": "2020-10-13T14:50:52.962141Z",
}

job_2 = {
    "id": 2,
    "source_type": "SRA",
    "success": False,
    "start_time": None,
    "end_time": None,
    "created_at": "2020-10-01T20:12:30.926574Z",
    "last_modified": "2020-10-01T20:12:32.836891Z",
}

search_1 = {"count": 2, "next": "search_2", "previous": None, "results": [job_1]}

search_2 = {"count": 2, "next": None, "previous": "search_1", "results": [job_2]}


def mock_request(method, url, **kwargs):

    if url == "https://api.refine.bio/v1/jobs/survey/1/":
        return MockResponse(job_1, url)

    if url == "https://api.refine.bio/v1/jobs/survey/2/":
        return MockResponse(job_2, url)

    if url == "https://api.refine.bio/v1/jobs/survey/0/":
        return MockResponse(None, url, status=404)

    if url == "https://api.refine.bio/v1/jobs/survey/500/":
        return MockResponse(None, url, status=500)

    if url == "https://api.refine.bio/v1/jobs/survey/":
        return MockResponse(search_1, "search_2")

    if url == "search_2":
        return MockResponse(search_2, url)


class SurveyJobTests(unittest.TestCase, CustomAssertions):
    @patch("pyrefinebio.api_interface.requests.request", side_effect=mock_request)
    def test_survey_job_get(self, mock_request):
        result = pyrefinebio.SurveyJob.get(1)
        self.assertObject(result, job_1)

    @patch("pyrefinebio.api_interface.requests.request", side_effect=mock_request)
    def test_survey_job_500(self, mock_request):
        with self.assertRaises(pyrefinebio.exceptions.ServerError):
            pyrefinebio.SurveyJob.get(500)

    @patch("pyrefinebio.api_interface.requests.request", side_effect=mock_request)
    def test_survey_job_get_404(self, mock_request):
        with self.assertRaises(pyrefinebio.exceptions.NotFound):
            pyrefinebio.SurveyJob.get(0)

    @patch("pyrefinebio.api_interface.requests.request", side_effect=mock_request)
    def test_survey_job_search_no_filters(self, mock_request):
        results = pyrefinebio.SurveyJob.search()

        self.assertObject(results[0], job_1)
        self.assertObject(results[1], job_2)

    def test_survey_job_search_with_filters(self):
        filtered_results = pyrefinebio.SurveyJob.search(id=214436, source_type="GEO", success=False)

        for result in filtered_results:
            self.assertEqual(result.id, 214436)
            self.assertEqual(result.source_type, "GEO")
            self.assertFalse(result.success)

    def test_survey_job_search_with_invalid_filters(self):
        with self.assertRaises(pyrefinebio.exceptions.InvalidFilters):
            pyrefinebio.SurveyJob.search(foo="bar")
