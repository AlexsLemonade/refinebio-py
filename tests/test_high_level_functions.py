import unittest
import pyrefinebio
import os
from pyrefinebio.config import Config
from unittest.mock import Mock, patch

from tests.custom_assertions import CustomAssertions
from tests.mocks import MockResponse


class HighLevelFunctionTests(unittest.TestCase, CustomAssertions):
    @patch("pyrefinebio.dataset.download_file")
    @patch("pyrefinebio.dataset.get_by_endpoint")
    @patch("pyrefinebio.dataset.post_by_endpoint")
    def test_download_dataset_dataset_dict(self, mock_post, mock_get, mock_download):
        mr = MockResponse(
            {"id": "test_dataset", "is_processed": True, "download_url": "test_url"}, "url"
        )

        mock_get.return_value = mr
        mock_post.return_value = mr

        dataset_dict = {"test": ["foo", "bar"]}

        pyrefinebio.download_dataset("test", "foo@test.com", dataset_dict=dataset_dict)

        mock_post.assert_called_with(
            "dataset",
            payload={
                "data": dataset_dict,
                "aggregate_by": "EXPERIMENT",
                "email_address": "foo@test.com",
                "start": True,
                "quantile_normalize": True,
                "quant_sf_only": False,
                "notify_me": False,
            },
        )

        mock_download.assert_called_with("test_url", os.path.abspath("test"), True)

    @patch("pyrefinebio.dataset.download_file")
    @patch("pyrefinebio.dataset.get_by_endpoint")
    @patch("pyrefinebio.dataset.post_by_endpoint")
    def test_download_dataset_notify_me(self, mock_post, mock_get, mock_download):
        mr = MockResponse(
            {"id": "test_dataset", "is_processed": True, "download_url": "test_url"}, "url"
        )

        mock_get.return_value = mr
        mock_post.return_value = mr

        dataset_dict = {"test": ["foo", "bar"]}

        pyrefinebio.download_dataset(
            "test", "foo@test.com", dataset_dict=dataset_dict, notify_me=True
        )

        mock_post.assert_called_with(
            "dataset",
            payload={
                "data": dataset_dict,
                "aggregate_by": "EXPERIMENT",
                "email_address": "foo@test.com",
                "start": True,
                "quantile_normalize": True,
                "quant_sf_only": False,
                "notify_me": True,
            },
        )

        mock_download.assert_called_with("test_url", os.path.abspath("test"), True)

    @patch("pyrefinebio.dataset.download_file")
    @patch("pyrefinebio.dataset.get_by_endpoint")
    @patch("pyrefinebio.dataset.post_by_endpoint")
    def test_download_dataset_experiments(self, mock_post, mock_get, mock_download):
        mr = MockResponse(
            {"id": "test_dataset", "is_processed": True, "download_url": "test_url"}, "url"
        )

        mock_get.return_value = mr
        mock_post.return_value = mr

        experiment2 = pyrefinebio.Experiment(accession_code="test-experiment-2")

        pyrefinebio.download_dataset(
            "test", "foo@test.com", experiments=["test-experiment-1", experiment2]
        )

        mock_post.assert_called_with(
            "dataset",
            payload={
                "data": {"test-experiment-1": ["ALL"], "test-experiment-2": ["ALL"]},
                "aggregate_by": "EXPERIMENT",
                "email_address": "foo@test.com",
                "start": True,
                "quantile_normalize": True,
                "quant_sf_only": False,
                "notify_me": False,
            },
        )

        mock_download.assert_called_with("test_url", os.path.abspath("test"), True)

    @patch("pyrefinebio.dataset.shutil.unpack_archive")
    @patch("pyrefinebio.dataset.download_file")
    @patch("pyrefinebio.dataset.get_by_endpoint")
    @patch("pyrefinebio.dataset.post_by_endpoint")
    def test_download_dataset_extract(self, mock_post, mock_get, mock_download, mock_unpack):
        mr = MockResponse(
            {"id": "test_dataset", "is_processed": True, "download_url": "test_url"}, "url"
        )

        mock_get.return_value = mr
        mock_post.return_value = mr

        dataset_dict = {"test": ["foo", "bar"]}

        pyrefinebio.download_dataset("./", "foo@test.com", dataset_dict=dataset_dict, extract=True)

        expected_path = os.path.abspath("dataset-test_dataset.zip")

        mock_download.assert_called_with("test_url", expected_path, True)
        mock_unpack.assert_called_with(expected_path)

    def test_download_dataset_both(self):
        with self.assertRaises(pyrefinebio.exceptions.DownloadError):
            pyrefinebio.download_dataset(
                "test", "foo@test.com", dataset_dict={"bad"}, experiments=["bad"]
            )

    @patch("pyrefinebio.compendia.download_file")
    @patch("pyrefinebio.compendia.get_by_endpoint")
    def test_download_compendium(self, mock_get, mock_download):
        mock_get.return_value = MockResponse(
            {
                "count": 1,
                "next": None,
                "previous": None,
                "results": [{"computed_file": {"download_url": "test_url"}}],
            },
            "url",
        )

        pyrefinebio.download_compendium("test", "test_organism")

        mock_get.assert_called_with(
            "compendia",
            params={
                "primary_organism__name": "test_organism",
                "quant_sf_only": False,
                "latest_version": True,
            },
        )

        mock_download.assert_called_with("test_url", os.path.abspath("test"), True)

    @patch("pyrefinebio.compendia.shutil.unpack_archive")
    @patch("pyrefinebio.compendia.download_file")
    @patch("pyrefinebio.compendia.get_by_endpoint")
    def test_download_compendium_extract(self, mock_get, mock_download, mock_unpack):
        mock_get.return_value = MockResponse(
            {
                "count": 1,
                "next": None,
                "previous": None,
                "results": [{"id": 123, "computed_file": {"download_url": "test_url"}}],
            },
            "url",
        )

        pyrefinebio.download_compendium("./", "test_organism", extract=True)

        expected_path = os.path.abspath("compendium-123.zip")

        mock_download.assert_called_with("test_url", expected_path, True)
        mock_unpack.assert_called_with(expected_path)

    def test_download_compendium_no_results(self):
        with self.assertRaises(pyrefinebio.exceptions.DownloadError):
            pyrefinebio.download_compendium("test", "this-will-have-no-results")

    @patch("pyrefinebio.computed_file.get_by_endpoint")
    @patch("pyrefinebio.compendia.get_by_endpoint")
    def test_download_compendium_no_token(self, mock_compendia_get, mock_computed_file_get):
        mock_compendia_get.return_value = MockResponse(
            {
                "count": 1,
                "next": None,
                "previous": None,
                "results": [{"computed_file": {"download_url": None}}],
            },
            "url",
        )

        mock_computed_file_get.return_value = MockResponse({"download_url": None}, "url")

        with self.assertRaises(pyrefinebio.exceptions.DownloadError):
            pyrefinebio.download_compendium("test", "test_organism")

    @patch("pyrefinebio.high_level_functions.Token")
    @patch("pyrefinebio.high_level_functions.input")
    def test_create_token_with_prompt(self, mock_input, mock_token):
        mock_input.return_value = "y"

        mock_created_token = pyrefinebio.create_token()

        self.assertTrue(mock_token.called)

        self.assertTrue(mock_created_token.agree_to_terms_and_conditions.called)
        self.assertTrue(mock_created_token.save_token.called)

    @patch("pyrefinebio.high_level_functions.Token")
    @patch("pyrefinebio.high_level_functions.input")
    def test_create_token_activate_no_save(self, mock_input, mock_token):
        mock_created_token = pyrefinebio.create_token(agree_to_terms=True, save_token=False)

        self.assertTrue(mock_token.called)

        self.assertTrue(mock_created_token.agree_to_terms_and_conditions.called)
        self.assertFalse(mock_created_token.save_token.called)
