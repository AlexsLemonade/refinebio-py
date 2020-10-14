import unittest
import pyrefinebio
from unittest.mock import Mock, patch

from .custom_assertions import CustomAssertions
from .mocks import MockResponse

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

    if url == "https://api.refine.bio/v1/qn_targets/DANIO_RERIO/":
        return MockResponse(processor_1, url)

    if url == "https://api.refine.bio/v1/qn_targets/HUMAN/":
        return MockResponse(None, url, status=404)

    if url == "https://api.refine.bio/v1/qn_targets/500/":
        return MockResponse(None, url, status=500)

    if url == "https://api.refine.bio/v1/qn_targets/":
        return MockResponse(qn_target_organisms, url)
