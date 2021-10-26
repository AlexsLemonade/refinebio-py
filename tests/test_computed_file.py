import os
import unittest
from unittest.mock import Mock, patch

import pyrefinebio
from tests.custom_assertions import CustomAssertions
from tests.mocks import MockResponse

computed_file_1 = {
    "id": 1,
    "filename": "salmontools-result.tar.gz",
    "samples": [
        {
            "accession_code": "SRR067392",
            "platform_name": "Illumina Genome Analyzer II",
            "pretty_platform": "Illumina Genome Analyzer II (IlluminaGenomeAnalyzerII)",
            "technology": "RNA-SEQ",
            "is_processed": True,
        }
    ],
    "size_in_bytes": 191,
    "is_qn_target": False,
    "is_smashable": False,
    "is_qc": True,
    "is_compendia": False,
    "quant_sf_only": False,
    "compendium_version": None,
    "sha1": "77ea7dd477fa9a9ec5f33bc91f46c0e224edeb92",
    "s3_bucket": "data-refinery-s3-circleci-prod",
    "s3_key": "gqo8hxhqm3tcz4c2x9sthhw5_salmontools-result.tar.gz",
    "s3_url": "https://s3.amazonaws.com/data-refinery-s3-circleci-prod/gqo8hxhqm3tcz4c2x9sthhw5_salmontools-result.tar.gz",
    "download_url": "test_download_url",
    "created_at": "2020-10-01T20:23:41.661425Z",
    "last_modified": "2020-10-01T20:23:42.378884Z",
    "result": {
        "id": 2784485,
        "commands": [
            "salmontools extract-unmapped -u /home/user/data_store/processor_job_29708301/SRR067392_output/aux_info/unmapped_names.txt -o /home/user/data_store/processor_job_29708301/salmontools/unmapped_by_salmon -r /home/user/data_store/processor_job_29708301/SRR067392.sra"
        ],
        "processor": {
            "id": 607,
            "name": "Salmontools",
            "version": "v1.39.5",
            "docker_image": "dr_salmon",
            "environment": {
                "os_pkg": {
                    "g++": "4:5.3.1-1ubuntu1",
                    "cmake": "3.5.1-1ubuntu3",
                    "python3": "3.5.1-3",
                    "python3-pip": "8.1.1-2ubuntu0.4",
                },
                "python": {"Django": "2.2.13", "data-refinery-common": "1.39.5"},
                "cmd_line": {"salmontools --version": "Salmon Tools 0.1.0"},
                "os_distribution": "Ubuntu 16.04.6 LTS",
            },
        },
        "is_ccdl": True,
        "annotations": [],
        "files": [
            {
                "id": 5836309,
                "filename": "salmontools-result.tar.gz",
                "size_in_bytes": 191,
                "is_smashable": False,
                "is_qc": True,
                "sha1": "77ea7dd477fa9a9ec5f33bc91f46c0e224edeb92",
                "s3_bucket": "data-refinery-s3-circleci-prod",
                "s3_key": "gqo8hxhqm3tcz4c2x9sthhw5_salmontools-result.tar.gz",
                "created_at": "2020-10-01T20:23:41.661425Z",
                "last_modified": "2020-10-01T20:23:42.378884Z",
            }
        ],
        "organism_index": None,
        "time_start": "2020-10-01T20:23:06.885498Z",
        "time_end": "2020-10-01T20:23:41.030134Z",
        "created_at": "2020-10-01T20:23:41.655614Z",
        "last_modified": "2020-10-01T20:23:41.655614Z",
    },
}

computed_file_2 = {
    "id": 2,
    "filename": "salmontools-result.tar.gz",
    "samples": [
        {
            "accession_code": "SRR067392",
            "platform_name": "Illumina Genome Analyzer II",
            "pretty_platform": "Illumina Genome Analyzer II (IlluminaGenomeAnalyzerII)",
            "technology": "RNA-SEQ",
            "is_processed": True,
        }
    ],
    "size_in_bytes": 191,
    "is_qn_target": False,
    "is_smashable": False,
    "is_qc": True,
    "is_compendia": False,
    "quant_sf_only": False,
    "compendium_version": None,
    "sha1": "77ea7dd477fa9a9ec5f33bc91f46c0e224edeb92",
    "s3_bucket": "data-refinery-s3-circleci-prod",
    "s3_key": "gqo8hxhqm3tcz4c2x9sthhw5_salmontools-result.tar.gz",
    "s3_url": "https://s3.amazonaws.com/data-refinery-s3-circleci-prod/gqo8hxhqm3tcz4c2x9sthhw5_salmontools-result.tar.gz",
    "created_at": "2020-10-01T20:23:41.661425Z",
    "last_modified": "2020-10-01T20:23:42.378884Z",
    "result": {
        "id": 2784485,
        "commands": [
            "salmontools extract-unmapped -u /home/user/data_store/processor_job_29708301/SRR067392_output/aux_info/unmapped_names.txt -o /home/user/data_store/processor_job_29708301/salmontools/unmapped_by_salmon -r /home/user/data_store/processor_job_29708301/SRR067392.sra"
        ],
        "processor": {
            "id": 607,
            "name": "Salmontools",
            "version": "v1.39.5",
            "docker_image": "dr_salmon",
            "environment": {
                "os_pkg": {
                    "g++": "4:5.3.1-1ubuntu1",
                    "cmake": "3.5.1-1ubuntu3",
                    "python3": "3.5.1-3",
                    "python3-pip": "8.1.1-2ubuntu0.4",
                },
                "python": {"Django": "2.2.13", "data-refinery-common": "1.39.5"},
                "cmd_line": {"salmontools --version": "Salmon Tools 0.1.0"},
                "os_distribution": "Ubuntu 16.04.6 LTS",
            },
        },
        "is_ccdl": True,
        "annotations": [],
        "files": [
            {
                "id": 5836309,
                "filename": "salmontools-result.tar.gz",
                "size_in_bytes": 191,
                "is_smashable": False,
                "is_qc": True,
                "sha1": "77ea7dd477fa9a9ec5f33bc91f46c0e224edeb92",
                "s3_bucket": "data-refinery-s3-circleci-prod",
                "s3_key": "gqo8hxhqm3tcz4c2x9sthhw5_salmontools-result.tar.gz",
                "created_at": "2020-10-01T20:23:41.661425Z",
                "last_modified": "2020-10-01T20:23:42.378884Z",
            }
        ],
        "organism_index": None,
        "time_start": "2020-10-01T20:23:06.885498Z",
        "time_end": "2020-10-01T20:23:41.030134Z",
        "created_at": "2020-10-01T20:23:41.655614Z",
        "last_modified": "2020-10-01T20:23:41.655614Z",
    },
}

result = {
    "id": 2784485,
    "commands": [
        "salmontools extract-unmapped -u /home/user/data_store/processor_job_29708301/SRR067392_output/aux_info/unmapped_names.txt -o /home/user/data_store/processor_job_29708301/salmontools/unmapped_by_salmon -r /home/user/data_store/processor_job_29708301/SRR067392.sra"
    ],
    "processor": {
        "id": 607,
        "name": "Salmontools",
        "version": "v1.39.5",
        "docker_image": "dr_salmon",
        "environment": {
            "os_pkg": {
                "g++": "4:5.3.1-1ubuntu1",
                "cmake": "3.5.1-1ubuntu3",
                "python3": "3.5.1-3",
                "python3-pip": "8.1.1-2ubuntu0.4",
            },
            "python": {"Django": "2.2.13", "data-refinery-common": "1.39.5"},
            "cmd_line": {"salmontools --version": "Salmon Tools 0.1.0"},
            "os_distribution": "Ubuntu 16.04.6 LTS",
        },
    },
    "is_ccdl": True,
    "annotations": [],
    "files": [
        {
            "id": 5836309,
            "filename": "salmontools-result.tar.gz",
            "size_in_bytes": 191,
            "is_smashable": False,
            "is_qc": True,
            "sha1": "77ea7dd477fa9a9ec5f33bc91f46c0e224edeb92",
            "s3_bucket": "data-refinery-s3-circleci-prod",
            "s3_key": "gqo8hxhqm3tcz4c2x9sthhw5_salmontools-result.tar.gz",
            "created_at": "2020-10-01T20:23:41.661425Z",
            "last_modified": "2020-10-01T20:23:42.378884Z",
        }
    ],
    "organism_index": None,
    "time_start": "2020-10-01T20:23:06.885498Z",
    "time_end": "2020-10-01T20:23:41.030134Z",
    "created_at": "2020-10-01T20:23:41.655614Z",
    "last_modified": "2020-10-01T20:23:41.655614Z",
}

search_1 = {"count": 2, "next": "search_2", "previous": None, "results": [computed_file_1]}

search_2 = {"count": 2, "next": None, "previous": "search_1", "results": [computed_file_2]}


def mock_request(method, url, **kwargs):

    if url == "https://api.refine.bio/v1/computed_files/1/":
        return MockResponse(computed_file_1, url)

    if url == "https://api.refine.bio/v1/computed_files/2/":
        return MockResponse(computed_file_2, url)

    if url == "https://api.refine.bio/v1/computed_files/0/":
        return MockResponse(None, url, status=404)

    if url == "https://api.refine.bio/v1/computed_files/500/":
        return MockResponse(None, url, status=500)

    if url == "https://api.refine.bio/v1/computed_files/":
        return MockResponse(search_1, "search_2")

    if url == "search_2":
        return MockResponse(search_2, url)

    if url == "https://api.refine.bio/v1/computational_results/2784485/":
        return MockResponse(result, url)


class ComputedFileTests(unittest.TestCase, CustomAssertions):
    @patch("pyrefinebio.api_interface.requests.request", side_effect=mock_request)
    def test_computed_file_get(self, mock_request):
        result = pyrefinebio.ComputedFile.get(1)
        self.assertObject(result, computed_file_1)

    @patch("pyrefinebio.api_interface.requests.request", side_effect=mock_request)
    def test_computed_file_500(self, mock_request):
        with self.assertRaises(pyrefinebio.exceptions.ServerError):
            pyrefinebio.ComputedFile.get(500)

    @patch("pyrefinebio.api_interface.requests.request", side_effect=mock_request)
    def test_computed_file_get_404(self, mock_request):
        with self.assertRaises(pyrefinebio.exceptions.NotFound):
            pyrefinebio.ComputedFile.get(0)

    @patch("pyrefinebio.api_interface.requests.request", side_effect=mock_request)
    def test_computed_file_search_no_filters(self, mock_request):
        results = pyrefinebio.ComputedFile.search()

        self.assertObject(results[0], computed_file_1)
        self.assertObject(results[1], computed_file_2)

    def test_computed_file_search_with_filters(self):
        filtered_results = pyrefinebio.ComputedFile.search(is_compendia=True, quant_sf_only=False)

        for result in filtered_results:
            self.assertTrue(result.is_compendia)
            self.assertFalse(result.quant_sf_only)

    def test_computed_file_search_with_invalid_filters(self):
        with self.assertRaises(pyrefinebio.exceptions.InvalidFilters):
            pyrefinebio.ComputedFile.search(foo="bar")

    # just mock download - it's already tested in depth in test_dataset
    @patch("pyrefinebio.computed_file.download_file")
    @patch("pyrefinebio.api_interface.requests.request", side_effect=mock_request)
    def test_computed_file_download(self, mock_request, mock_download):
        result = pyrefinebio.ComputedFile.get(1)

        result.download("test-path")

        mock_download.assert_called_with("test_download_url", os.path.abspath("test-path"), True)

    @patch("pyrefinebio.api_interface.requests.request", side_effect=mock_request)
    def test_computed_file_download_no_url(self, mock_request):
        result = pyrefinebio.ComputedFile.get(2)  # 2 has no download_url

        with self.assertRaises(pyrefinebio.exceptions.DownloadError) as de:
            result.download("test-path")

    @patch("pyrefinebio.computed_file.shutil.unpack_archive")
    def test_computed_file_extract(self, mock_unpack):
        cf = pyrefinebio.ComputedFile()

        cf._downloaded_path = "foo"

        cf.extract()

        mock_unpack.assert_called_with("foo")

    def test_computed_file_samples_are_fully_populated(self):
        # ComputedFile.Sample looks like this when retrieved from the API
        # We should make sure that the other sample properties are populated properly
        # {
        #     "accession_code": "SRR067392",
        #     "platform_name": "Illumina Genome Analyzer II",
        #     "pretty_platform": "Illumina Genome Analyzer II (IlluminaGenomeAnalyzerII)",
        #     "technology": "RNA-SEQ",
        #     "is_processed": True
        # }

        cfs = pyrefinebio.ComputedFile.search()
        cf = next(cf for cf in cfs if cf.samples)

        self.assertIsNotNone(cf.samples[0].experiment_accession_codes)
        self.assertIsNotNone(cf.samples[0].source_database)
        self.assertIsNotNone(cf.samples[0].organism)
        self.assertIsNotNone(cf.samples[0].platform_accession_code)
        self.assertIsNotNone(cf.samples[0].pretty_platform)
        self.assertIsNotNone(cf.samples[0].manufacturer)
