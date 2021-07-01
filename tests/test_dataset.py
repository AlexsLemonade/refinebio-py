import json
import os
import unittest
from unittest.mock import Mock, patch

import pyrefinebio
from pyrefinebio.config import Config
from tests.custom_assertions import CustomAssertions
from tests.mocks import MockResponse

dataset = {
    "id": "test-dataset",
    "data": {"test-experiment": ["sample-1", "sample-2"]},
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
    "svd_algorithm": "NONE",
}

non_processed_dataset = {
    "id": "non-processed-dataset",
    "is_processing": False,
    "is_processed": False,
    "download_url": None,
}


def mock_request(method, url, data, **kwargs):

    if method == "POST":
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

    if url == "https://api.refine.bio/v1/dataset/non-processed-dataset/":
        return MockResponse(non_processed_dataset, url)

    if url == "https://api.refine.bio/v1/dataset/":
        return MockResponse(dataset, url)

    if url == "https://api.refine.bio/v1/dataset/500/":
        return MockResponse(dataset, url, status=500)


class DatasetTests(unittest.TestCase, CustomAssertions):
    @classmethod
    def tearDownClass(cls):
        os.environ.pop("REFINEBIO_CONFIG_FILE", None)

    @patch("pyrefinebio.api_interface.requests.request", side_effect=mock_request)
    def test_dataset_get(self, mock_request):
        result = pyrefinebio.Dataset.get("test-dataset")
        self.assertObject(result, dataset)

    def test_dataset_get_404(self):
        with self.assertRaises(pyrefinebio.exceptions.NotFound):
            pyrefinebio.Dataset.get("this-does-not-exist")

    @patch("pyrefinebio.api_interface.requests.request", side_effect=mock_request)
    def test_dataset_500(self, mock_request):
        with self.assertRaises(pyrefinebio.exceptions.ServerError):
            pyrefinebio.Dataset.get("500")

    @patch("pyrefinebio.dataset.post_by_endpoint")
    @patch("pyrefinebio.dataset.put_by_endpoint")
    def test_dataset_save(self, mock_put, mock_post):
        mock_post.return_value = MockResponse(dataset, "")
        mock_put.return_value = MockResponse(dataset, "")

        ds = pyrefinebio.Dataset(
            data={"test-experiment": ["sample-1", "sample-2"]}, email_address="test-email"
        )
        ds = ds.save()

        mock_post.assert_called_with(
            "dataset",
            payload={
                "data": {"test-experiment": ["sample-1", "sample-2"]},
                "email_address": "test-email",
                "notify_me": False,
            },
        )

        ds.email_address = "changed-email"
        ds.save()

        mock_put.assert_called_with(
            "dataset/test-dataset",
            payload={
                "data": {"test-experiment": ["sample-1", "sample-2"]},
                "aggregate_by": "EXPERIMENT",
                "scale_by": "NONE",
                "email_address": "changed-email",
                "quantile_normalize": True,
                "quant_sf_only": False,
                "svd_algorithm": "NONE",
                # We want email notifications to be opt-out
                "notify_me": False,
            },
        )

    def test_dataset_save_bad_data(self):
        with self.assertRaises(pyrefinebio.exceptions.InvalidData):
            pyrefinebio.Dataset(data={"lol": ["not-good"]}).save()

    @patch("pyrefinebio.dataset.post_by_endpoint")
    def test_dataset_skip_quantile_normalization(self, mock_post_by_endpoint):
        """
        Test skipping quantile normalization

        Test the corner case brought up by Steven where we set
        quantile_normalize False. We used to check if quantile_normalize was
        truthy before adding it to the request, which caused it to always be
        true.
        """

        pyrefinebio.Dataset(
            data={"GSE68833": ["ALL"]},
            aggregate_by="EXPERIMENT",
            email_address="foo@bar.com",
            quantile_normalize=False,
        ).save()

        self.assertEqual(mock_post_by_endpoint.call_count, 1)

        # We need to use assertEqual here because None is False-y
        args, kwargs = mock_post_by_endpoint.call_args
        self.assertEqual(kwargs["payload"].get("quantile_normalize", None), False)

    @patch("pyrefinebio.dataset.post_by_endpoint")
    @patch("pyrefinebio.dataset.put_by_endpoint")
    def test_dataset_notify_me(self, mock_put_by_endpoint, mock_post_by_endpoint):
        """
        Test requesting to be notified
        """
        mock_post_by_endpoint.return_value = MockResponse(dataset, "")

        # First test that notify_me is false by default
        ds = pyrefinebio.Dataset(
            data={"GSE68833": ["ALL"]},
            aggregate_by="EXPERIMENT",
            email_address="foo@bar.com",
        )
        ds.save()

        self.assertEqual(mock_post_by_endpoint.call_count, 1)

        # We need to use assertEqual here because None is False-y
        args, kwargs = mock_post_by_endpoint.call_args
        self.assertEqual(kwargs["payload"].get("notify_me", None), False)

        self.assertIsNotNone(ds.id)

        # Now set notify_me true
        ds.notify_me = True
        ds.save()

        self.assertEqual(mock_put_by_endpoint.call_count, 1)

        args, kwargs = mock_put_by_endpoint.call_args
        self.assertTrue(kwargs["payload"].get("notify_me", None))

    @patch("pyrefinebio.api_interface.requests.request", side_effect=mock_request)
    def test_dataset_process(self, mock_request):
        ds = pyrefinebio.Dataset(
            data={"test-experiment": ["sample-1", "sample-2"]}, email_address="test-email"
        )
        ds.process()

        self.assertTrue(ds.start)
        self.assertTrue(ds.is_processing)

    def test_dataset_process_bad_token(self):
        pyrefinebio.config.Config().token = "this-is-a-bad-token"

        data = {}
        exs = pyrefinebio.Experiment.search(num_downloadable_samples=1)
        ex = next(exs)
        data[ex.accession_code] = ["ALL"]

        ds = pyrefinebio.Dataset(data=data)

        with self.assertRaises(pyrefinebio.exceptions.BadRequest) as br:
            ds.process()

        self.assertEqual(
            br.exception.base_message, "Bad Request: You must provide an active API token ID"
        )

    def test_dataset_process_no_email(self):
        try:
            token = pyrefinebio.Token(id="42240c84-b3d9-4f41-8001-6f40abce9d7d")
            token.agree_to_terms_and_conditions()
        except pyrefinebio.exceptions.NotFound:
            token = pyrefinebio.Token()
            token.agree_to_terms_and_conditions()

        data = {}
        exs = pyrefinebio.Experiment.search(num_downloadable_samples=1)
        ex = next(exs)
        data[ex.accession_code] = ["ALL"]

        ds = pyrefinebio.Dataset(data=data)

        with self.assertRaises(pyrefinebio.exceptions.BadRequest) as br:
            ds.process()

        self.assertEqual(
            br.exception.base_message, "Bad Request: You must provide an email address."
        )

    @patch("pyrefinebio.api_interface.requests.request", side_effect=mock_request)
    def test_dataset_check(self, mock_request):
        ds = pyrefinebio.Dataset(id="test-dataset")
        is_done = ds.check()

        self.assertTrue(is_done)
        self.assertTrue(ds.is_processing)
        self.assertTrue(ds.is_processed)

    @patch("pyrefinebio.api_interface.shutil.copyfileobj")
    @patch("pyrefinebio.api_interface.open")
    @patch("pyrefinebio.api_interface.requests.get")
    def test_dataset_download(self, mock_get, mock_open, mock_copy):
        ds = pyrefinebio.Dataset(download_url="test_download_url")

        mr = MockResponse(None, "test_download_url", headers={"content-length": 3})

        setattr(mr, "raw", "raw")

        mock_get.return_value.__enter__.return_value = mr
        mock_open.return_value.__enter__.return_value = "file"

        ds.download("test_path")

        mock_get.assert_called_with("test_download_url", stream=True)
        mock_open.assert_called_with(os.path.abspath("test_path"), "wb")
        mock_copy.assert_called_with("raw", "file")

    @patch("pyrefinebio.api_interface.shutil.copyfileobj")
    @patch("pyrefinebio.api_interface.input")
    @patch("pyrefinebio.api_interface.requests.get")
    def test_dataset_download_big_file(self, mock_get, mock_input, mock_copy):
        ds = pyrefinebio.Dataset(download_url="test_download_url")

        mr = MockResponse(None, "test_download_url", headers={"content-length": 1000000000000})

        setattr(mr, "raw", "raw")

        mock_get.return_value.__enter__.return_value = mr
        mock_input.return_value = "n"

        ds.download("test_path")

        mock_get.assert_called_with("test_download_url", stream=True)
        mock_copy.assert_not_called()

    @patch("pyrefinebio.api_interface.requests.request", side_effect=mock_request)
    def test_dataset_download_no_url(self, mock_request):
        ds = pyrefinebio.Dataset(id="non-processed-dataset", download_url=None)
        with self.assertRaises(pyrefinebio.exceptions.DownloadError) as de:
            ds.download("test")

        self.assertEqual(
            str(de.exception),
            "Unable to download Dataset\nDownload url not found - you must process the Dataset before downloading.",
        )

    @patch("pyrefinebio.api_interface.shutil.copyfileobj")
    @patch("pyrefinebio.api_interface.input")
    @patch("pyrefinebio.api_interface.requests.get")
    def test_dataset_download_no_size_header(self, mock_get, mock_input, mock_copy):
        ds = pyrefinebio.Dataset(download_url="test_download_url")

        mr = MockResponse(None, "test_download_url", headers={})

        setattr(mr, "raw", "raw")

        mock_get.return_value.__enter__.return_value = mr
        mock_input.return_value = "n"

        ds.download("test_path")

        mock_get.assert_called_with("test_download_url", stream=True)
        mock_copy.assert_not_called()

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
                "test-experiment-3": ["sample1", "sample2", "sample3"],
            },
        )

    @patch("pyrefinebio.dataset.shutil.unpack_archive")
    def test_dataset_extract(self, mock_unpack):
        ds = pyrefinebio.Dataset()

        ds._downloaded_path = "foo"

        ds.extract()

        mock_unpack.assert_called_with("foo")
