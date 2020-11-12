import unittest
import pyrefinebio
from unittest.mock import Mock, patch

from tests.custom_assertions import CustomAssertions
from tests.mocks import MockResponse


computed_file_1 = {
    "id": 5836309,
    "filename": "salmontools-result.tar.gz",
    "samples": [
        {
            "accession_code": "SRR067392",
            "platform_name": "Illumina Genome Analyzer II",
            "pretty_platform": "Illumina Genome Analyzer II (IlluminaGenomeAnalyzerII)",
            "technology": "RNA-SEQ",
            "is_processed": True
        }
    ],
    "size_in_bytes": 191,
    "is_qn_target": False,
    "is_smashable": False,
    "is_qc": True,
    "is_compendia": False,
    "quant_sf_only": False,
    "compendia_version": None,
    "sha1": "77ea7dd477fa9a9ec5f33bc91f46c0e224edeb92",
    "s3_bucket": "data-refinery-s3-circleci-prod",
    "s3_key": "gqo8hxhqm3tcz4c2x9sthhw5_salmontools-result.tar.gz",
    "s3_url": "https://s3.amazonaws.com/data-refinery-s3-circleci-prod/gqo8hxhqm3tcz4c2x9sthhw5_salmontools-result.tar.gz",
    "download_url": "https://data-refinery-s3-circleci-prod.s3.amazonaws.com/gqo8hxhqm3tcz4c2x9sthhw5_salmontools-result.tar.gz?X-Amz-Algorithm=AWS4-HMAC-SHA256&X-Amz-Credential=ASIAYSVVCNE545GJ4DP5%2F20201008%2Fus-east-1%2Fs3%2Faws4_request&X-Amz-Date=20201008T190717Z&X-Amz-Expires=604800&X-Amz-SignedHeaders=host&X-Amz-Security-Token=IQoJb3JpZ2luX2VjEPv%2F%2F%2F%2F%2F%2F%2F%2F%2F%2FwEaCXVzLWVhc3QtMSJHMEUCIFS9gjbsRxcVwxgE2SOF%2B1aGzsJzDTeF9cJqS7TXg7fBAiEApWf2yVT7yl4kgVVEE37doQTDZEzoUpYTabinRKiXROoqtAMINBABGgw1ODk4NjQwMDM4OTkiDDwu6a4uA9fA%2FpLUWiqRA9FrrpW7HGp8o%2BTgeKarp5fJBxQC%2FMfWHQSuaM%2BUMUGZoT5DWSI0D37APfw52Jgb5c6J%2FO7pt0UL721AzB8mVkGQmiuVshfsBmJBK5l7gq9H6gcKB2D21brhvPciXf7HrTdMf%2Fr3xcFu3iux%2B0yu6C6gj19xI7FepOhGEsh%2FZD1UshsSzQEonGxOrwhBGQj6ge7UXW4M5SDPRrXPXDt6Qmm%2FdeDptns9Gr6sqtq969BE3G61uz2FEEUELcye8U544sk8rGuGhDSwzaSeY6sxytxjWSylFPlETlp0kLLmJtLxBqe0X3cjNN7W0MybNtj7RVHApgByY4DLAS7h4xOEpLrZgQfsr9phF%2FYaZKKrTV1UUIvk%2BQgUNPDPN5yrBjrY%2FHB9eegYiw9YoI6k%2FaK4TRI6LT7POfYsRkkZBRi2hqCdcwYjXZX6s3wonmFuJiCYZ%2B3yi5eGg6LKe8yoO1UvbiFLABCMKk6h2fDYlPtbupLyRpGqjt3FPyPsq37y7MyZS8AFzAmiXgjVENuLRO3IGqKaMKO3%2FfsFOusBVWVEsZwZvX%2BuDjd%2BpMrMt%2FZbrCcGoaIVrGIkrNxilAIGzH4YfbK8CNgQVWpjmezL6ayA5fBNNajW9XQJfVOFDKEiB5o5dD4fzM1Aahj6orQJ5Y7P1pNdPU4y05auGkcIxygt%2BbY6g%2F%2FMZ0ca6ofU0m9qrsgyzPjot38hWRDlo%2BTYyNjYqOQCt5gsFX0MXO43R2wZ%2FPNUl8VH9Mo3L80M%2Fa7gv%2FXdYpZHQWzC8jia6dygolN2OGzpK5VSZa48EnT8zc%2B7y2S9asKnrAhSOwb7BaCGz2eFMWqZz9jcys6nad6R2P4Zldh4ilopig%3D%3D&X-Amz-Signature=abb7cc628781043a9afd41bf4c0114c26f27a22c8940b94befe07448b8f71a49",
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
                    "python3-pip": "8.1.1-2ubuntu0.4"
                },
                "python": {
                    "Django": "2.2.13",
                    "data-refinery-common": "1.39.5"
                },
                "cmd_line": {
                    "salmontools --version": "Salmon Tools 0.1.0"
                },
                "os_distribution": "Ubuntu 16.04.6 LTS"
            }
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
                "last_modified": "2020-10-01T20:23:42.378884Z"
            }
        ],
        "organism_index": None,
        "time_start": "2020-10-01T20:23:06.885498Z",
        "time_end": "2020-10-01T20:23:41.030134Z",
        "created_at": "2020-10-01T20:23:41.655614Z",
        "last_modified": "2020-10-01T20:23:41.655614Z"
    }
}

computed_file_2 = {
    "id": 5836309,
    "filename": "salmontools-result.tar.gz",
    "samples": [
        {
            "accession_code": "SRR067392",
            "platform_name": "Illumina Genome Analyzer II",
            "pretty_platform": "Illumina Genome Analyzer II (IlluminaGenomeAnalyzerII)",
            "technology": "RNA-SEQ",
            "is_processed": True
        }
    ],
    "size_in_bytes": 191,
    "is_qn_target": False,
    "is_smashable": False,
    "is_qc": True,
    "is_compendia": False,
    "quant_sf_only": False,
    "compendia_version": None,
    "sha1": "77ea7dd477fa9a9ec5f33bc91f46c0e224edeb92",
    "s3_bucket": "data-refinery-s3-circleci-prod",
    "s3_key": "gqo8hxhqm3tcz4c2x9sthhw5_salmontools-result.tar.gz",
    "s3_url": "https://s3.amazonaws.com/data-refinery-s3-circleci-prod/gqo8hxhqm3tcz4c2x9sthhw5_salmontools-result.tar.gz",
    "download_url": "https://data-refinery-s3-circleci-prod.s3.amazonaws.com/gqo8hxhqm3tcz4c2x9sthhw5_salmontools-result.tar.gz?X-Amz-Algorithm=AWS4-HMAC-SHA256&X-Amz-Credential=ASIAYSVVCNE545GJ4DP5%2F20201008%2Fus-east-1%2Fs3%2Faws4_request&X-Amz-Date=20201008T190717Z&X-Amz-Expires=604800&X-Amz-SignedHeaders=host&X-Amz-Security-Token=IQoJb3JpZ2luX2VjEPv%2F%2F%2F%2F%2F%2F%2F%2F%2F%2FwEaCXVzLWVhc3QtMSJHMEUCIFS9gjbsRxcVwxgE2SOF%2B1aGzsJzDTeF9cJqS7TXg7fBAiEApWf2yVT7yl4kgVVEE37doQTDZEzoUpYTabinRKiXROoqtAMINBABGgw1ODk4NjQwMDM4OTkiDDwu6a4uA9fA%2FpLUWiqRA9FrrpW7HGp8o%2BTgeKarp5fJBxQC%2FMfWHQSuaM%2BUMUGZoT5DWSI0D37APfw52Jgb5c6J%2FO7pt0UL721AzB8mVkGQmiuVshfsBmJBK5l7gq9H6gcKB2D21brhvPciXf7HrTdMf%2Fr3xcFu3iux%2B0yu6C6gj19xI7FepOhGEsh%2FZD1UshsSzQEonGxOrwhBGQj6ge7UXW4M5SDPRrXPXDt6Qmm%2FdeDptns9Gr6sqtq969BE3G61uz2FEEUELcye8U544sk8rGuGhDSwzaSeY6sxytxjWSylFPlETlp0kLLmJtLxBqe0X3cjNN7W0MybNtj7RVHApgByY4DLAS7h4xOEpLrZgQfsr9phF%2FYaZKKrTV1UUIvk%2BQgUNPDPN5yrBjrY%2FHB9eegYiw9YoI6k%2FaK4TRI6LT7POfYsRkkZBRi2hqCdcwYjXZX6s3wonmFuJiCYZ%2B3yi5eGg6LKe8yoO1UvbiFLABCMKk6h2fDYlPtbupLyRpGqjt3FPyPsq37y7MyZS8AFzAmiXgjVENuLRO3IGqKaMKO3%2FfsFOusBVWVEsZwZvX%2BuDjd%2BpMrMt%2FZbrCcGoaIVrGIkrNxilAIGzH4YfbK8CNgQVWpjmezL6ayA5fBNNajW9XQJfVOFDKEiB5o5dD4fzM1Aahj6orQJ5Y7P1pNdPU4y05auGkcIxygt%2BbY6g%2F%2FMZ0ca6ofU0m9qrsgyzPjot38hWRDlo%2BTYyNjYqOQCt5gsFX0MXO43R2wZ%2FPNUl8VH9Mo3L80M%2Fa7gv%2FXdYpZHQWzC8jia6dygolN2OGzpK5VSZa48EnT8zc%2B7y2S9asKnrAhSOwb7BaCGz2eFMWqZz9jcys6nad6R2P4Zldh4ilopig%3D%3D&X-Amz-Signature=abb7cc628781043a9afd41bf4c0114c26f27a22c8940b94befe07448b8f71a49",
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
                    "python3-pip": "8.1.1-2ubuntu0.4"
                },
                "python": {
                    "Django": "2.2.13",
                    "data-refinery-common": "1.39.5"
                },
                "cmd_line": {
                    "salmontools --version": "Salmon Tools 0.1.0"
                },
                "os_distribution": "Ubuntu 16.04.6 LTS"
            }
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
                "last_modified": "2020-10-01T20:23:42.378884Z"
            }
        ],
        "organism_index": None,
        "time_start": "2020-10-01T20:23:06.885498Z",
        "time_end": "2020-10-01T20:23:41.030134Z",
        "created_at": "2020-10-01T20:23:41.655614Z",
        "last_modified": "2020-10-01T20:23:41.655614Z"
    }
}

search_1 = {
    "count": 2,
    "next": "search_2",
    "previous": None,
    "results": [computed_file_1]
}

search_2 = {
    "count": 2,
    "next": None,
    "previous": "search_1",
    "results": [computed_file_2]
}

def mock_request(method, url, **kwargs):

    if url == "https://api.refine.bio/v1/computed_files/1/":
        return MockResponse(computed_file_1, url)

    if url == "https://api.refine.bio/v1/computed_files/0/":
        return MockResponse(None, url, status=404)

    if url == "https://api.refine.bio/v1/computed_files/500/":
        return MockResponse(None, url, status=500)

    if url == "https://api.refine.bio/v1/computed_files/":
        return MockResponse(search_1, "search_2")

    if url == "search_2":
        return MockResponse(search_2, url)

class ComputedFileTests(unittest.TestCase, CustomAssertions):

    @patch("pyrefinebio.http.requests.request", side_effect=mock_request)
    def test_computed_file_get(self, mock_request):
        result = pyrefinebio.ComputedFile.get(1)
        self.assertObject(result, computed_file_1)


    @patch("pyrefinebio.http.requests.request", side_effect=mock_request)
    def test_computed_file_500(self, mock_request):
        with self.assertRaises(pyrefinebio.exceptions.ServerError):
            pyrefinebio.ComputedFile.get(500)


    @patch("pyrefinebio.http.requests.request", side_effect=mock_request)
    def test_computed_file_get_404(self, mock_request):
        with self.assertRaises(pyrefinebio.exceptions.NotFound):
            pyrefinebio.ComputedFile.get(0)


    @patch("pyrefinebio.http.requests.request", side_effect=mock_request)
    def test_computed_file_search_no_filters(self, mock_request):
        result = pyrefinebio.ComputedFile.search()

        result_list = list(result)

        self.assertObject(result_list[0], computed_file_1)
        self.assertObject(result_list[1], computed_file_2)

        self.assertEqual(len(mock_request.call_args_list), 2)


    def test_computed_file_search_with_filters(self):
        filtered_results = pyrefinebio.ComputedFile.search(is_compendia=True, quant_sf_only=False)

        for result in filtered_results:
            self.assertTrue(result.is_compendia)
            self.assertFalse(result.quant_sf_only)


    def test_computed_file_search_with_invalid_filters(self):
        with self.assertRaises(pyrefinebio.exceptions.InvalidFilters):
            pyrefinebio.ComputedFile.search(foo="bar")
