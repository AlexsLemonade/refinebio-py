import unittest
import pyrefinebio
from unittest.mock import Mock, patch

from .custom_assertions import CustomAssertions


institutions = [
    {
        "submitter_institution": "Drexel University"
    },
    {
        "submitter_institution": "University of Pennsylvania"
    },
    {
        "submitter_institution": "NYU MEDICAL SCHOOL"
    },
    {
        "submitter_institution": "Villanova University"
    }
]


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

    if url == "https://api.refine.bio/v1/institutions/":
        return MockResponse(institutions)


class ComputedFileTests(unittest.TestCase, CustomAssertions):

    @patch("pyrefinebio.http.requests.request", side_effect=mock_request)
    def test_computed_file_get(self, mock_request):
        result = pyrefinebio.Institution.search()

        self.assertEqual(len(result), len(institutions))

        for i in range(len(result)):
            self.assertObject(result[i], institutions[i])
