import unittest
import pyrefinebio
from unittest.mock import Mock, patch

from .custom_assertions import CustomAssertions

experiment = {
    "id": 0,
    "title": "test",
    "description": "test experiment",
    "annotations": [
        {
        "data": "test",
        "is_ccdl": True,
        "created_at": "2020-10-02T18:48:24Z",
        "last_modified": "2020-10-02T18:48:24Z"
        }
    ],
    "samples": [
        {
        "accession_code": "test",
        "platform_name": "test",
        "pretty_platform": "test",
        "technology": "test",
        "is_processed": True
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
    "publication_authors": [
        "string"
    ],
    "pubmed_id": "string",
    "source_first_published": "2020-10-02T18:48:24Z",
    "source_last_modified": "2020-10-02T18:48:24Z",
    "submitter_institution": "string",
    "last_modified": "2020-10-02T18:48:24Z",
    "created_at": "2020-10-02T18:48:24Z",
    "organism_names": [
        "string"
    ],
    "sample_metadata": "string",
    "num_total_samples": 1,
    "num_processed_samples": 1,
    "num_downloadable_samples": 1
}

experiment_search_result_1 = {
    "id": 69,
    "title": "test title 1",
    "publication_title": "test title 1",
    "description": "test description 1",
    "technology": "RNA-SEQ",
    "accession_code": "SRP150473",
    "alternate_accession_code": "GSE115746",
    "submitter_institution": "UPenn",
    "has_publication": True,
    "publication_doi": "",
    "publication_authors": [
        "Tate S",
        "Shapiro J"
    ],
    "sample_metadata_fields": [
        "specimen_part",
        "disease",
        "subject"
    ],
    "platform_names": [
        "Illumina HiSeq 2500"
    ],
    "platform_accession_codes": [
        "IlluminaHiSeq2500"
    ],
    "organism_names": [],
    "pubmed_id": "30382198",
    "num_total_samples": 28706,
    "num_processed_samples": 0,
    "num_downloadable_samples": 0,
    "source_first_published": "2018-11-02T00:00:00+00:00"
}

experiment_search_result_2 = {
    "id": 42,
    "title": "test title 2",
    "publication_title": "test title 2",
    "description": "test description 2",
    "technology": "RNA-SEQ",
    "accession_code": "SRP150473",
    "alternate_accession_code": "GSE115746",
    "submitter_institution": "Drexel",
    "has_publication": True,
    "publication_doi": "",
    "publication_authors": [
        "Wheeler K",
        "Mejia D"
    ],
    "sample_metadata_fields": [
        "specimen_part",
        "disease",
        "subject"
    ],
    "platform_names": [
        "Illumina HiSeq 2500"
    ],
    "platform_accession_codes": [
        "IlluminaHiSeq2500"
    ],
    "organism_names": [
        "HUMAN",
        "GORILLA"
    ],
    "pubmed_id": "30382198",
    "num_total_samples": 28706,
    "num_processed_samples": 0,
    "num_downloadable_samples": 0,
    "source_first_published": "2018-11-02T00:00:00+00:00"
}

search_1 = {
    "count": 2,
    "next": "search_2",
    "previous": None,
    "results": [experiment_search_result_1]
}

search_2 = {
    "count": 2,
    "next": None,
    "previous": "search_1",
    "results": [experiment_search_result_2]
}

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

    if url == "https://api.refine.bio/v1/experiments/SRP150473/":
        return MockResponse(experiment)

    if url == "https://api.refine.bio/v1/experiments/0/":
        return MockResponse(None, status=404)

    if url == "https://api.refine.bio/v1/experiments/500/":
        return MockResponse(None, status=500)

    if url == "https://api.refine.bio/v1/search/":
        return MockResponse(search_1)

    if url == "search_2":
        return MockResponse(search_2)

class ExperimentTests(unittest.TestCase, CustomAssertions):

    @patch("pyrefinebio.http.requests.request", side_effect=mock_request)
    def test_experiments_get(self, mock_request):
        result = pyrefinebio.Experiment.get("SRP150473")
        self.assertObject(result, experiment)


    @patch("pyrefinebio.http.requests.request", side_effect=mock_request)
    def test_experiments_500(self, mock_request):
        with self.assertRaises(Exception):
            pyrefinebio.Experiment.get(500)


    @patch("pyrefinebio.http.requests.request", side_effect=mock_request)
    def test_experiments_get_404(self, mock_request):
        with self.assertRaises(Exception):
            pyrefinebio.Experiment.get(0)


    @patch("pyrefinebio.http.requests.request", side_effect=mock_request)
    def test_experiments_search_no_filters(self, mock_request):
        result = pyrefinebio.Experiment.search()

        result_list = list(result)

        self.assertObject(result_list[0], experiment_search_result_1)
        self.assertObject(result_list[1], experiment_search_result_2)

        self.assertEqual(len(mock_request.call_args_list), 2)


    def test_experiments_search_with_filters(self):
        pass


    #TODO: validate filters on search endpoint
    def test_experiments_search_with_invalid_filters(self):
        with self.assertRaises(Exception):
            pyrefinebio.Experiment.search(foo="bar")
