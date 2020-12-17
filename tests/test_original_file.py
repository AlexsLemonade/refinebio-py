import unittest
import pyrefinebio
from unittest.mock import Mock, patch

from tests.custom_assertions import CustomAssertions
from tests.mocks import MockResponse


og_file_1 = {
    "id": 1,
    "filename": "SRR067396.sra",
    "size_in_bytes": 1004703052,
    "sha1": "cdef439e998b12e5f58a89b92f5a96d01aecbe75",
    "samples": [
        {
            "accession_code": "SRR067396",
            "platform_name": "Illumina Genome Analyzer II",
            "pretty_platform": "Illumina Genome Analyzer II (IlluminaGenomeAnalyzerII)",
            "technology": "RNA-SEQ",
            "is_processed": True
        }
    ],
    "processor_jobs": [
        {
            "id": 29708302,
            "pipeline_applied": "SALMON",
            "num_retries": 0,
            "retried": False,
            "worker_id": "i-0ea363205be30776f",
            "ram_amount": 12288,
            "volume_index": "i-0ea363205be30776f",
            "worker_version": "v1.39.5",
            "failure_reason": None,
            "nomad_job_id": "SALMON_i-0ea363205be30776f_12288/dispatch-1601583545-daff9ed4",
            "success": True,
            "original_files": [
                2925811
            ],
            "datasets": [],
            "start_time": "2020-10-01T20:20:04.109061Z",
            "end_time": "2020-10-01T20:23:43.507988Z",
            "created_at": "2020-10-01T20:19:05.841594Z",
            "last_modified": "2020-10-01T20:23:43.508066Z"
        }
    ],
    "downloader_jobs": [
        {
            "id": 7381811,
            "downloader_task": "SRA",
            "num_retries": 0,
            "retried": False,
            "was_recreated": False,
            "worker_id": "i-0ea363205be30776f",
            "worker_version": "v1.39.5",
            "nomad_job_id": "DOWNLOADER_i-0ea363205be30776f_4096/dispatch-1601583299-b70b4a3f",
            "failure_reason": None,
            "success": True,
            "original_files": [
                2925811
            ],
            "start_time": "2020-10-01T20:18:23.079796Z",
            "end_time": "2020-10-01T20:19:05.873400Z",
            "created_at": "2020-10-01T20:14:59.668642Z",
            "last_modified": "2020-10-01T20:19:05.873426Z"
        },
        {
            "id": 7381790,
            "downloader_task": "SRA",
            "num_retries": -1,
            "retried": True,
            "was_recreated": False,
            "worker_id": "i-0ea363205be30776f",
            "worker_version": "v1.39.5",
            "nomad_job_id": "DOWNLOADER_i-0ea363205be30776f_1024/dispatch-1601583197-afd6e327",
            "failure_reason": None,
            "success": False,
            "original_files": [
                2925811
            ],
            "start_time": "2020-10-01T20:13:28.201378Z",
            "end_time": None,
            "created_at": "2020-10-01T20:13:07.850264Z",
            "last_modified": "2020-10-01T20:14:59.693663Z"
        }
    ],
    "source_url": "anonftp@ftp-private.ncbi.nlm.nih.gov:/sra/sra-instant/reads/ByRun/sra/SRR/SRR067/SRR067396/SRR067396.sra",
    "source_filename": "SRR067396.sra",
    "is_downloaded": False,
    "is_archive": False,
    "has_raw": True,
    "created_at": "2020-10-01T20:13:03.302659Z",
    "last_modified": "2020-10-01T20:23:43.278755Z"
}

og_file_list_1 = {
    "id": 3,
    "filename": "GSM2351172_A52084400939855091415421246947329.CEL",
    "samples": [
        123456
    ],
    "size_in_bytes": 69357911,
    "sha1": "9a7068160ae899de6bb245f5e35982a4810cb36e",
    "processor_jobs": [
        123456
    ],
    "downloader_jobs": [],
    "source_url": "ftp://ftp.ncbi.nlm.nih.gov/geo/samples/GSM2351nnn/GSM2351172/suppl/GSM2351172_A52084400939855091415421246947329.CEL.gz",
    "is_archive": False,
    "source_filename": "GSM2351172_A52084400939855091415421246947329.CEL.gz",
    "has_raw": True,
    "created_at": "2020-10-13T23:03:56.233937Z",
    "last_modified": "2020-10-13T23:03:56.233937Z"
}

og_file_list_2 = {
    "id": 4,
    "filename": "GSM2351172_A52084400939855091415421246947329.CEL",
    "samples": [
        123456,
        224564
    ],
    "size_in_bytes": 69357911,
    "sha1": "9a7068160ae899de6bb245f5e35982a4810cb36e",
    "processor_jobs": [
        123456,
        222111,
        444333
    ],
    "downloader_jobs": [
        123456,
        123457,
        123458
    ],
    "source_url": "ftp://ftp.ncbi.nlm.nih.gov/geo/samples/GSM2351nnn/GSM2351172/suppl/GSM2351172_A52084400939855091415421246947329.CEL.gz",
    "is_archive": True,
    "source_filename": "GSM2351172_A52084400939855091415421246947329.CEL.gz",
    "has_raw": True,
    "created_at": "2020-10-13T23:03:56.233937Z",
    "last_modified": "2020-10-13T23:03:56.233937Z"
}

search_1 = {
    "count": 2,
    "next": "search_2",
    "previous": None,
    "results": [og_file_list_1]
}

search_2 = {
    "count": 2,
    "next": None,
    "previous": "search_1",
    "results": [og_file_list_2]
}

def mock_request(method, url, **kwargs):

    if url == "https://api.refine.bio/v1/original_files/1/":
        return MockResponse(og_file_1, url)

    if url == "https://api.refine.bio/v1/original_files/0/":
        return MockResponse(None, url, status=404)

    if url == "https://api.refine.bio/v1/original_files/500/":
        return MockResponse(None, url, status=500)

    if url == "https://api.refine.bio/v1/original_files/":
        return MockResponse(search_1, "search_2")

    if url == "search_2":
        return MockResponse(search_2, url)

class OriginalFileTests(unittest.TestCase, CustomAssertions):

    @patch("pyrefinebio.http.requests.request", side_effect=mock_request)
    def test_original_file_get(self, mock_request):
        result = pyrefinebio.OriginalFile.get(1)
        self.assertObject(result, og_file_1)


    @patch("pyrefinebio.http.requests.request", side_effect=mock_request)
    def test_original_file_500(self, mock_request):
        with self.assertRaises(pyrefinebio.exceptions.ServerError):
            pyrefinebio.OriginalFile.get(500)


    @patch("pyrefinebio.http.requests.request", side_effect=mock_request)
    def test_original_file_get_404(self, mock_request):
        with self.assertRaises(pyrefinebio.exceptions.NotFound):
            pyrefinebio.OriginalFile.get(0)


    @patch("pyrefinebio.http.requests.request", side_effect=mock_request)
    def test_original_file_search_no_filters(self, mock_request):
        result = pyrefinebio.OriginalFile.search()

        result_list = list(result)

        self.assertObject(result_list[0], og_file_list_1)
        self.assertObject(result_list[1], og_file_list_2)

        self.assertEqual(len(mock_request.call_args_list), 2)


    def test_original_file_search_with_filters(self):
        filtered_results = pyrefinebio.OriginalFile.search(size_in_bytes=1000)

        for result in filtered_results:
            self.assertEqual(result.size_in_bytes, 1000)


    def test_original_file_search_with_invalid_filters(self):
        with self.assertRaises(pyrefinebio.exceptions.InvalidFilters):
            pyrefinebio.OriginalFile.search(foo="bar")
