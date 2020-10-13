import unittest
import pyrefinebio
from unittest.mock import Mock, patch

from .custom_assertions import CustomAssertions

qn_target_organisms = [
    {
        "name": "MUSTELA_PUTORIUS_FURO",
        "taxonomy_id": 9669
    },
    {
        "name": "RATTUS_NORVEGICUS",
        "taxonomy_id": 10116
    },
    {
        "name": "ARABIDOPSIS_THALIANA",
        "taxonomy_id": 3702
    },
    {
        "name": "MUSCULUS",
        "taxonomy_id": 112137
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

    if url == "https://api.refine.bio/v1/qn_targets/DANIO_RERIO/":
        return MockResponse(processor_1)

    if url == "https://api.refine.bio/v1/qn_targets/HUMAN/":
        return MockResponse(None, status=404)

    if url == "https://api.refine.bio/v1/qn_targets/500/":
        return MockResponse(None, status=500)

    if url == "https://api.refine.bio/v1/qn_targets/":
        return MockResponse(qn_target_organisms)
