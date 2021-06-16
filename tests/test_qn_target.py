import unittest
from unittest.mock import Mock, patch

import pyrefinebio
from tests.custom_assertions import CustomAssertions
from tests.mocks import MockResponse

qn_target_organisms = [
    {"name": "MUSTELA_PUTORIUS_FURO", "taxonomy_id": 9669},
    {"name": "RATTUS_NORVEGICUS", "taxonomy_id": 10116},
    {"name": "ARABIDOPSIS_THALIANA", "taxonomy_id": 3702},
    {"name": "MUSCULUS", "taxonomy_id": 112137},
]

qn_target = {
    "id": 5741412,
    "filename": "1574800731_target.tsv",
    "size_in_bytes": 318754,
    "is_qn_target": True,
    "sha1": "bb04eb22101c4b25509aae0f2bd0e60763fd053d",
    "s3_bucket": "data-refinery-s3-qn-target-circleci-prod",
    "s3_key": "eo9yywkbvjcc1lj9s0qegnt4_1574800731_target.tsv",
    "s3_url": "https://s3.amazonaws.com/data-refinery-s3-qn-target-circleci-prod/eo9yywkbvjcc1lj9s0qegnt4_1574800731_target.tsv",
    "created_at": "2019-11-26T20:39:29.309489Z",
    "last_modified": "2019-11-26T20:39:29.610226Z",
    "result": {
        "id": 2722294,
        "commands": ["q n _ r e f e r e n c e . p y"],
        "processor": {
            "id": 527,
            "name": "Quantile Normalization Reference",
            "version": "v1.29.6-hotfix",
            "docker_image": "dr_smasher",
            "environment": {
                "R": {"preprocessCore": "1.42.0"},
                "os_pkg": {
                    "r-base": "r-base",
                    "python3": "3.5.1-3",
                    "python3-pip": "8.1.1-2ubuntu0.4",
                },
                "python": {
                    "rpy2": "2.9.5",
                    "Django": "2.2.7",
                    "pandas": "0.23.4",
                    "data-refinery-common": "=v1.29.6-hotfix",
                },
                "os_distribution": "Ubuntu 16.04.6 LTS",
            },
        },
        "is_ccdl": True,
        "annotations": [
            {
                "id": 2790940,
                "data": {
                    "is_qn": True,
                    "geneset": "['ENSCAFG00000025287', 'ENSCAFG00000008570', 'ENSCAFG00000018001']",
                    "samples": ["GSM1540469", "GSM297356", "GSM879434", "GSM879435", "GSM879436"],
                    "organism_id": 28,
                    "num_valid_inputs": 146,
                    "platform_accession_code": "canine2",
                },
                "is_ccdl": True,
                "created_at": "2019-11-26T20:39:29.317850Z",
                "last_modified": "2019-11-26T20:39:29.317850Z",
            }
        ],
        "organism_index": None,
        "time_start": "2019-11-26T20:38:51.632946Z",
        "time_end": "2019-11-26T20:39:28.534756Z",
        "created_at": "2019-11-26T20:39:29.303846Z",
        "last_modified": "2019-11-26T20:39:29.303846Z",
    },
}


def mock_request(method, url, **kwargs):

    if url == "https://api.refine.bio/v1/qn_targets/MUSTELA_PUTORIUS_FURO/":
        return MockResponse(qn_target, url)

    if url == "https://api.refine.bio/v1/qn_targets/HUMAN/":
        return MockResponse(None, url, status=404)

    if url == "https://api.refine.bio/v1/qn_targets/500/":
        return MockResponse(None, url, status=500)

    if url == "https://api.refine.bio/v1/qn_targets/":
        return MockResponse(qn_target_organisms, url)


class QNTargetTests(unittest.TestCase, CustomAssertions):
    @patch("pyrefinebio.api_interface.requests.request", side_effect=mock_request)
    def test_qn_target_get(self, mock_request):
        result = pyrefinebio.QNTarget.get("MUSTELA_PUTORIUS_FURO")
        self.assertObject(result, qn_target)

    @patch("pyrefinebio.api_interface.requests.request", side_effect=mock_request)
    def test_qn_target_500(self, mock_request):
        with self.assertRaises(Exception):
            pyrefinebio.QNTarget.get(500)

    @patch("pyrefinebio.api_interface.requests.request", side_effect=mock_request)
    def test_qn_target_404(self, mock_request):
        with self.assertRaises(Exception):
            pyrefinebio.QNTarget.get(0)

    @patch("pyrefinebio.api_interface.requests.request", side_effect=mock_request)
    def test_qn_target_search(self, mock_request):
        result = pyrefinebio.QNTarget.search()

        self.assertEqual(len(result), len(qn_target_organisms))

        for i in range(len(result)):
            self.assertObject(result[i], qn_target_organisms[i])
