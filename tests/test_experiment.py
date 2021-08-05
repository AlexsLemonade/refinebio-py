import unittest
from unittest.mock import Mock, patch

import pyrefinebio
from tests.custom_assertions import CustomAssertions
from tests.mocks import MockResponse

experiment = {
    "id": 0,
    "title": "test",
    "description": "test experiment",
    "annotations": [
        {
            "data": "test",
            "is_ccdl": True,
            "created_at": "2020-10-02T18:48:24Z",
            "last_modified": "2020-10-02T18:48:24Z",
        }
    ],
    "samples": [
        {
            "accession_code": "test",
            "platform_name": "test",
            "pretty_platform": "test",
            "technology": "test",
            "is_processed": True,
        }
    ],
    "protocol_description": "string",
    "accession_code": "string",
    "alternate_accession_code": "string",
    "source_database": "string",
    "source_url": "string",
    "has_publication": True,
    "publication_title": "string",
    "publication_doi": "string",
    "publication_authors": ["string"],
    "pubmed_id": "string",
    "source_first_published": "2020-10-02T18:48:24Z",
    "source_last_modified": "2020-10-02T18:48:24Z",
    "submitter_institution": "string",
    "last_modified": "2020-10-02T18:48:24Z",
    "created_at": "2020-10-02T18:48:24Z",
    "organism_names": ["string"],
    "sample_metadata": "string",
    "num_total_samples": 1,
    "num_processed_samples": 1,
    "num_downloadable_samples": 1,
}

experiment_search_result_1 = {
    "id": 42,
    "title": "test title 1",
    "publication_title": "test title 1",
    "description": "test description 1",
    "technology": "RNA-SEQ",
    "accession_code": "SRP150473",
    "alternate_accession_code": "GSE115746",
    "submitter_institution": "UPenn",
    "has_publication": True,
    "publication_doi": "",
    "publication_authors": ["Tate S", "Shapiro J"],
    "sample_metadata_fields": ["specimen_part", "disease", "subject"],
    "platform_names": ["Illumina HiSeq 2500"],
    "platform_accession_codes": ["IlluminaHiSeq2500"],
    "organism_names": ["HUMAN"],
    "pubmed_id": "30382198",
    "num_total_samples": 28706,
    "num_processed_samples": 0,
    "num_downloadable_samples": 0,
    "source_first_published": "2018-05-31T00:00:00Z",
}

experiment_search_result_2 = {
    "id": 43,
    "title": "test title 2",
    "publication_title": "test title 2",
    "description": "test description 2",
    "technology": "RNA-SEQ",
    "accession_code": "SRP150473",
    "alternate_accession_code": "GSE115746",
    "submitter_institution": "Drexel",
    "has_publication": True,
    "publication_doi": "",
    "publication_authors": ["Wheeler K", "Mejia D"],
    "sample_metadata_fields": ["specimen_part", "disease", "subject"],
    "platform_names": ["Illumina HiSeq 2500"],
    "platform_accession_codes": ["IlluminaHiSeq2500"],
    "organism_names": ["HUMAN", "GORILLA"],
    "pubmed_id": "30382198",
    "num_total_samples": 28706,
    "num_processed_samples": 0,
    "num_downloadable_samples": 0,
    "source_first_published": "2018-05-31T00:00:00Z",
}

search_1 = {
    "count": 2,
    "next": "search_2",
    "previous": None,
    "results": [experiment_search_result_1],
}

search_2 = {
    "count": 2,
    "next": None,
    "previous": "search_1",
    "results": [experiment_search_result_2],
}


def mock_request(method, url, **kwargs):

    if url == "https://api.refine.bio/v1/experiments/SRP150473/":
        return MockResponse(experiment, url)

    if url == "https://api.refine.bio/v1/experiments/bad-accession-code/":
        return MockResponse(None, url, status=404)

    if url == "https://api.refine.bio/v1/experiments/force-500-error/":
        return MockResponse(None, url, status=500)

    if url == "https://api.refine.bio/v1/search/":
        return MockResponse(search_1, "search_2")

    if url == "search_2":
        return MockResponse(search_2, url)


class ExperimentTests(unittest.TestCase, CustomAssertions):
    @patch("pyrefinebio.api_interface.requests.request", side_effect=mock_request)
    def test_experiments_get(self, mock_request):
        result = pyrefinebio.Experiment.get("SRP150473")
        self.assertObject(result, experiment)

    @patch("pyrefinebio.api_interface.requests.request", side_effect=mock_request)
    def test_experiments_500(self, mock_request):
        with self.assertRaises(pyrefinebio.exceptions.ServerError):
            pyrefinebio.Experiment.get("force-500-error")

    @patch("pyrefinebio.api_interface.requests.request", side_effect=mock_request)
    def test_experiments_get_404(self, mock_request):
        with self.assertRaises(pyrefinebio.exceptions.NotFound):
            pyrefinebio.Experiment.get("bad-accession-code")

    @patch("pyrefinebio.api_interface.requests.request", side_effect=mock_request)
    def test_experiments_search_no_filters(self, mock_request):
        results = pyrefinebio.Experiment.search()

        self.assertObject(results[0], experiment_search_result_1)
        self.assertObject(results[1], experiment_search_result_2)

    def test_experiments_search_with_filters(self):
        filtered_results = pyrefinebio.Experiment.search(
            num_downloadable_samples=20, has_publication="true"
        )  # TODO: investigate why True breaks this endpoint

        for result in filtered_results:
            self.assertEqual(result.num_downloadable_samples, 20)
            self.assertTrue(result.has_publication)
