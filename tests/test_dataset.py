import unittest
import pyrefinebio
import os
import json
from pyrefinebio.config import Config
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

    if method == 'POST':
        data = json.loads(data)
        ds = {}
        for key, value in dataset.items():
            if data.get(key):
                ds[key] = data.get(key)
            else:
                ds[key] = value
        return MockResponse(ds, url)

    if url == "https://api.refine.bio/v1/dataset/test-dataset/":
        return MockResponse(dataset, url)

    if url == "https://api.refine.bio/v1/dataset/":
        return MockResponse(dataset, url)

    if url == "https://api.refine.bio/v1/dataset/500/":
        return MockResponse(dataset, url, status=500)


class DatasetTests(unittest.TestCase, CustomAssertions):

    @classmethod
    def tearDownClass(cls):
        os.environ.pop("CONFIG_FILE", None)

    @patch("pyrefinebio.http.requests.request", side_effect=mock_request)
    def test_dataset_get(self, mock_request):
        result = pyrefinebio.Dataset.get("test-dataset")
        self.assertObject(result, dataset)


    def test_dataset_get_404(self):
        with self.assertRaises(pyrefinebio.exceptions.NotFound):
            pyrefinebio.Dataset.get("this-does-not-exist")

    
    @patch("pyrefinebio.http.requests.request", side_effect=mock_request)
    def test_dataset_500(self, mock_request):
        with self.assertRaises(pyrefinebio.exceptions.ServerError):
            pyrefinebio.Dataset.get("500")


    @patch("pyrefinebio.dataset.post_by_endpoint")
    @patch("pyrefinebio.dataset.put_by_endpoint")
    def test_dataset_save(self, mock_put, mock_post):
        mock_post.return_value = MockResponse(dataset, "")
        mock_put.return_value = MockResponse(dataset, "")

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


    def test_dataset_save_bad_data(self):
        with self.assertRaises(pyrefinebio.exceptions.InvalidData):
            pyrefinebio.Dataset(data={"lol": ["not-good"]}).save()


    @patch("pyrefinebio.http.requests.request", side_effect=mock_request)
    def test_dataset_process(self, mock_request):
        ds = pyrefinebio.Dataset(data={"test-experiment": ["sample-1", "sample-2"]}, email_address="test-email")
        ds.process()

        self.assertTrue(ds.start)
        self.assertTrue(ds.is_processing)


    @patch("pyrefinebio.config.os.path.exists")
    @patch("pyrefinebio.config.yaml.full_load")
    @patch("pyrefinebio.config.open")
    def test_dataset_process_bad_token(self, mock_open, mock_load, mock_exists):
        Config._instance = None
        os.environ["CONFIG_FILE"] = "./temp"
        mock_open.return_value.__enter__.return_value = "file"
        mock_load.return_value = {"token": "this-is-a-bad-token"}
        mock_exists.return_value = True

        data = {}
        exs = pyrefinebio.Experiment.search(num_downloadable_samples=1)
        ex = next(exs)
        data[ex.accession_code] = ["ALL"]

        ds = pyrefinebio.Dataset(data=data)

        with self.assertRaises(pyrefinebio.exceptions.BadRequest) as br:
            ds.process()
        
        self.assertEqual(br.exception.base_message, "Bad Request: You must provide an active API token ID")

    
    @patch("pyrefinebio.config.os.path.exists")
    @patch("pyrefinebio.config.yaml.full_load")
    @patch("pyrefinebio.config.open")
    def test_dataset_process_no_email(self, mock_open, mock_load, mock_exists):
        Config._instance = None
        os.environ["CONFIG_FILE"] = "./temp"
        mock_open.return_value.__enter__.return_value = "file"
        mock_load.return_value = {"token": "42240c84-b3d9-4f41-8001-6f40abce9d7d"}
        mock_exists.return_value = True

        try:
            token = pyrefinebio.Token.get_token()
            pyrefinebio.Token.agree_to_terms_and_conditions(token)
        except pyrefinebio.exceptions.NotFound:
            token = pyrefinebio.Token.create_token("")
            pyrefinebio.Token.agree_to_terms_and_conditions(token)

        data = {}
        exs = pyrefinebio.Experiment.search(num_downloadable_samples=1)
        ex = next(exs)
        data[ex.accession_code] = ["ALL"]

        ds = pyrefinebio.Dataset(data=data)
        
        with self.assertRaises(pyrefinebio.exceptions.BadRequest) as br:
            ds.process()

        self.assertEqual(br.exception.base_message, "Bad Request: You must provide an email address.")


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

    
    def test_add_samples(self):
        dataset = pyrefinebio.Dataset()

        dataset.add_samples("test-experiment-1")

        experiment2 = pyrefinebio.Experiment(accession_code="test-experiment-2")

        dataset.add_samples(experiment2)

        sample1 = pyrefinebio.Sample(accession_code="sample1")
        sample2 = pyrefinebio.Sample(accession_code="sample2")

        dataset.add_samples("test-experiment-3", samples=[sample1, sample2, "sample3"])

        self.assertDictEqual(
            dataset.data,
            {
                "test-experiment-1": ["ALL"],
                "test-experiment-2": ["ALL"],
                "test-experiment-3": [
                    "sample1",
                    "sample2",
                    "sample3"
                ]
            }
        )
