import unittest

from unittest.mock import Mock, patch
from click.testing import CliRunner

from pyrefinebio.script import cli

class ScriptTests(unittest.TestCase):

    def setUp(self):
        self.runner = CliRunner()


    @patch("pyrefinebio.script.hlf.download_dataset")
    def test_download_dataset_dataset_dict(self, mock_download_dataset):
        self.runner.invoke(
            cli,
            [
                "download-dataset",
                "--path",          "./test.zip",
                "--email-address", "foo@bar.net",
                "--dataset-dict",  '{"foo": ["bar"]}'
            ]
        )

        mock_download_dataset.assert_called_with(
            "./test.zip",
            "foo@bar.net",
            {"foo": ["bar"]},
            None,
            "EXPERIMENT",
            "NONE",
            False
        )


    @patch("pyrefinebio.script.hlf.download_dataset")
    def test_download_dataset_experiments(self, mock_download_dataset):
        self.runner.invoke(
            cli,
            [
                "download-dataset",
                "--path",          "./test.zip",
                "--email-address", "foo@bar.net",
                "--experiments",  "foo bar baz"
            ]
        )

        mock_download_dataset.assert_called_with(
            "./test.zip",
            "foo@bar.net",
            None,
            ["foo", "bar", "baz"],
            "EXPERIMENT",
            "NONE",
            False
        )

    
    def test_download_dataset_both(self):
        result = self.runner.invoke(
            cli,
            [
                "download-dataset",
                "--path",          "./test.zip",
                "--email-address", "foo@bar.net",
                "--dataset-dict",  '{"foo": ["bar"]}',
                "--experiments",  "foo bar baz"
            ]
        )

        self.assertEqual(result.exit_code, 1)
        self.assertEqual(
            result.output,
            "Error: Unable to download Dataset\nYou should either provide dataset_dict or experiments but not both\n"
        )


    @patch("pyrefinebio.script.hlf.download_compendium")
    def test_download_compendium(self, mock_download_compendium):
        self.runner.invoke(
            cli,
            [
                "download-compendium",
                "--path",          "./test.zip",
                "--organism",      "foo",
                "--quant-sf-only", "true"
            ]
        )

        mock_download_compendium.assert_called_with(
            "./test.zip",
            "foo",
            True
        )


    @patch("pyrefinebio.script.hlf.download_quandfile_compendium")
    def test_download_compendium(self, mock_download_q_compendium):
        self.runner.invoke(
            cli,
            [
                "download-quandfile-compendium",
                "--path",          "./test.zip",
                "--organism",      "foo"
            ]
        )

        mock_download_q_compendium.assert_called_with(
            "./test.zip",
            "foo"
        )

    def test_download_compendium_bad_organism(self):
        result = self.runner.invoke(
            cli,
            [
                "download-compendium",
                "--path",          "./test.zip",
                "--organism",      "foo",
            ]
        )

        self.assertEqual(result.exit_code, 1)
        self.assertEqual(
            result.output,
            "Error: Unable to download Compendium\nCould not find any Compendium " +
            "with organism name, foo, version False, and quant_sf_only, False\n"
        )

