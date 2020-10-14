import unittest
import pyrefinebio
from unittest.mock import Mock, patch

from .custom_assertions import CustomAssertions
from .mocks import MockResponse


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

    if url == "https://api.refine.bio/v1/institutions/":
        return MockResponse(institutions, url)


class ComputedFileTests(unittest.TestCase, CustomAssertions):

    @patch("pyrefinebio.http.requests.request", side_effect=mock_request)
    def test_computed_file_get(self, mock_request):
        result = pyrefinebio.Institution.search()

        self.assertEqual(len(result), len(institutions))

        for i in range(len(result)):
            self.assertObject(result[i], institutions[i])
