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
            {
                "id": "test_dataset",
                "is_processed": True,
                "download_url": "test_url"
            },
            "url"
        )

        mock_get.return_value = mr
        mock_post.return_value = mr

        dataset_dict = {
            "test": ["foo", "bar"]
        }

        pyrefinebio.download_dataset("test", "foo@test.com", dataset_dict=dataset_dict)

        mock_post.assert_called_with(
            "dataset",
            payload={
                "data": dataset_dict,
                "aggregate_by": "EXPERIMENT",
                "email_address": "foo@test.com",
                "start": True,
                "quantile_normalize": True
            }
        )

        mock_download.assert_called_with("test_url", "test")


    @patch("pyrefinebio.dataset.download_file")
    @patch("pyrefinebio.dataset.get_by_endpoint")
    @patch("pyrefinebio.dataset.post_by_endpoint")
    def test_download_dataset_experiments(self, mock_post, mock_get, mock_download):
        mr = MockResponse(
            {
                "id": "test_dataset",
                "is_processed": True,
                "download_url": "test_url"
            },
            "url"
        )

        mock_get.return_value = mr
        mock_post.return_value = mr

        experiment2 = pyrefinebio.Experiment(accession_code="test-experiment-2")

        pyrefinebio.download_dataset("test", "foo@test.com", experiments=["test-experiment-1", experiment2])

        mock_post.assert_called_with(
            "dataset",
            payload={
                "data": {
                    "test-experiment-1": ["ALL"],
                    "test-experiment-2": ["ALL"]
                },
                "aggregate_by": "EXPERIMENT",
                "email_address": "foo@test.com",
                "start": True,
                "quantile_normalize": True
            }
        )

        mock_download.assert_called_with("test_url", "test")


    def test_download_dataset_both(self):
        with self.assertRaises(pyrefinebio.exceptions.DownloadError):
            pyrefinebio.download_dataset("test", "foo@test.com", dataset_dict={"bad"}, experiments=["bad"])


    @patch("pyrefinebio.high_level_functions.download_file")
    @patch("pyrefinebio.compendia.get_by_endpoint")
    def test_download_compendium(self, mock_get, mock_download):
        mock_get.return_value = MockResponse(
            {
                "count": 1,
                "next": None,
                "previous": None,
                "results": [
                    {
                        "computed_file": {
                            "download_url": "test_url"
                        }
                    }
                ]
            },
            "url"
        )

        pyrefinebio.download_compendium("test", "test_organism")
        
        mock_get.assert_called_with(
            "compendia",
            params={
                "primary_organism__name": "test_organism",
                "quant_sf_only": False,
                "latest_version": True
            }
        )

        mock_download.assert_called_with("test_url", "test")


    def test_download_compendium_no_results(self):
        with self.assertRaises(pyrefinebio.exceptions.DownloadError):
            pyrefinebio.download_compendium("test", "this-will-have-no-results")


    @patch("pyrefinebio.compendia.get_by_endpoint")
    def test_download_compendium_no_token(self, mock_get):
        mock_get.return_value = MockResponse(
            {
                "count": 1,
                "next": None,
                "previous": None,
                "results": [
                    {
                        "computed_file": {
                            "download_url": None
                        }
                    }
                ]
            },
            "url"
        )

        with self.assertRaises(pyrefinebio.exceptions.DownloadError):
            pyrefinebio.download_compendium("test", "test_organism")
