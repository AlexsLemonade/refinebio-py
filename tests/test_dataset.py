import unittest
import pyrefinebio
from unittest.mock import Mock, patch

from tests.custom_assertions import CustomAssertions
from tests.mocks import MockResponse


dataset = {
    "id": "test-dataset",
    "data": {
        "test-experiment": [
            "sample-1",
            "sample-2"
        ]
    },
    "aggregate_by": "EXPERIMENT",
    "scale_by": "NONE",
    "is_processing": True,
    "is_processed": True,
    "is_available": True,
    "has_email": True,
    "expires_on": "2020-10-29T16:12:56.449529Z",
    "s3_bucket": "test-bucket",
    "s3_key": "test-key",
    "success": True,
    "failure_reason": "",
    "created_at": "2020-10-19T19:30:36.157340Z",
    "last_modified": "2020-10-22T16:12:56.449544Z",
    "start": None,
    "size_in_bytes": 173109,
    "sha1": "test-sha1",
    "download_url": "test-dl-url",
    "quantile_normalize": True,
    "quant_sf_only": False,
    "svd_algorithm": "NONE"
}


def mock_request(method, url, data, **kwargs):

    if url == "https://api.refine.bio/v1/dataset/test-dataset/":
        return MockResponse(dataset, url)

    if url == "https://api.refine.bio/v1/dataset/":
        return MockResponse(dataset, url)


class DatasetTests(unittest.TestCase, CustomAssertions):

    @patch("pyrefinebio.http.requests.request", side_effect=mock_request)
    def test_dataset_get(self, mock_request):
        result = pyrefinebio.Dataset.get("test-dataset")
        self.assertObject(result, dataset)


    @patch("pyrefinebio.dataset.post_by_endpoint")
    @patch("pyrefinebio.dataset.put_by_endpoint")
    def test_dataset_save(self, mock_put, mock_post):
        mock_post.return_value = dataset

        ds = pyrefinebio.Dataset(data={"test-experiment": ["sample-1", "sample-2"]}, email_address="test-email")
        ds = ds.save()

        mock_post.assert_called_with(
            "dataset",
            payload={
                "data": {"test-experiment": ["sample-1", "sample-2"]},
                "email_address": "test-email"
            }
        )
    
        ds.email_address = "changed-email"
        ds.save()

        mock_put.assert_called_with(
            "dataset/test-dataset",
            payload={
                "data": {"test-experiment": ["sample-1", "sample-2"]},
                "aggregate_by": "EXPERIMENT",
                'scale_by': 'NONE',
                'email_address': 'changed-email',
                'quantile_normalize': True,
                'svd_algorithm': 'NONE'
            }
        )


    @patch("pyrefinebio.http.requests.request", side_effect=mock_request)
    def test_dataset_process(self, mock_request):
        ds = pyrefinebio.Dataset(data={"test-experiment": ["sample-1", "sample-2"]}, email_address="test-email")
        ds.process()

        self.assertTrue(ds.start)
        self.assertTrue(ds.is_processing)


    @patch("pyrefinebio.http.requests.request", side_effect=mock_request)
    def test_dataset_check(self, mock_request):
        ds = pyrefinebio.Dataset(id="test-dataset")
        is_done = ds.check()

        self.assertTrue(is_done)
        self.assertTrue(ds.is_processing)
        self.assertTrue(ds.is_processed)


    @patch("pyrefinebio.http.shutil.copyfileobj")
    @patch("pyrefinebio.http.open")
    @patch("pyrefinebio.http.requests.get")
    def test_dataset_download(self, mock_get, mock_open, mock_copy):
        mr = MockResponse({}, "test")
        setattr(mr, "raw", "raw")
        mock_get.return_value.__enter__.return_value = mr
        mock_open.return_value.__enter__.return_value = "file"

        ds = pyrefinebio.Dataset(download_url="test")
        ds.download("test")

        mock_get.assert_called_with("test", stream=True)
        mock_open.assert_called_with("test", "wb")
        mock_copy.assert_called_with("raw", "file")
