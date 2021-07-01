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
                "--email-address",
                "foo@bar.net",
                "--path",
                "./test.zip",
                "--dataset-dict",
                '{"foo": ["bar"]}',
            ],
        )

        mock_download_dataset.assert_called_with(
            "./test.zip",
            "foo@bar.net",
            {"foo": ["bar"]},
            None,
            "EXPERIMENT",
            "NONE",
            False,
            timeout=None,
            notify_me=False,
        )

    @patch("pyrefinebio.script.hlf.download_dataset")
    def test_download_dataset_notify_me(self, mock_download_dataset):
        self.runner.invoke(
            cli,
            [
                "download-dataset",
                "--email-address",
                "foo@bar.net",
                "--path",
                "./test.zip",
                "--dataset-dict",
                '{"foo": ["bar"]}',
                "--notify-me",
            ],
        )

        mock_download_dataset.assert_called_with(
            "./test.zip",
            "foo@bar.net",
            {"foo": ["bar"]},
            None,
            "EXPERIMENT",
            "NONE",
            False,
            timeout=None,
            notify_me=True,
        )

    @patch("pyrefinebio.script.hlf.download_dataset")
    def test_download_dataset_experiments(self, mock_download_dataset):
        self.runner.invoke(
            cli,
            [
                "download-dataset",
                "--email-address",
                "foo@bar.net",
                "--path",
                "./test.zip",
                "--experiments",
                "foo bar baz",
            ],
        )

        mock_download_dataset.assert_called_with(
            "./test.zip",
            "foo@bar.net",
            None,
            ["foo", "bar", "baz"],
            "EXPERIMENT",
            "NONE",
            False,
            timeout=None,
            notify_me=False,
        )

    @patch("pyrefinebio.script.hlf.download_dataset")
    def test_download_dataset_defualt_path(self, mock_download_dataset):
        self.runner.invoke(
            cli,
            ["download-dataset", "--email-address", "foo@bar.net", "--experiments", "foo bar baz"],
        )

        mock_download_dataset.assert_called_with(
            "./",
            "foo@bar.net",
            None,
            ["foo", "bar", "baz"],
            "EXPERIMENT",
            "NONE",
            False,
            timeout=None,
            notify_me=False,
        )

    def test_download_dataset_both(self):
        result = self.runner.invoke(
            cli,
            [
                "download-dataset",
                "--email-address",
                "foo@bar.net",
                "--path",
                "./test.zip",
                "--dataset-dict",
                '{"foo": ["bar"]}',
                "--experiments",
                "foo bar baz",
            ],
        )

        self.assertEqual(result.exit_code, 1)
        self.assertEqual(
            result.output,
            "Error: Unable to download Dataset\nYou should either provide dataset_dict or experiments but not both\n",
        )

    @patch("pyrefinebio.script.hlf.download_compendium")
    def test_download_compendium(self, mock_download_compendium):
        self.runner.invoke(
            cli,
            [
                "download-compendium",
                "--organism",
                "foo",
                "--path",
                "./test.zip",
                "--quant-sf-only",
                "true",
            ],
        )

        mock_download_compendium.assert_called_with("./test.zip", "foo", True)

    @patch("pyrefinebio.script.hlf.download_quantfile_compendium")
    def test_download_quantpendium(self, mock_download_q_compendium):
        self.runner.invoke(
            cli, ["download-quantfile-compendium", "--organism", "foo", "--path", "./test.zip"]
        )

        mock_download_q_compendium.assert_called_with("./test.zip", "foo")

    def test_download_compendium_bad_organism(self):
        result = self.runner.invoke(
            cli, ["download-compendium", "--organism", "foo", "--path", "./test.zip"]
        )

        self.assertEqual(result.exit_code, 1)
        self.assertEqual(
            result.output,
            "Searching for Compendium...\n"
            "Error: Unable to download Compendium\nCould not find any Compendium "
            + "with organism name, foo, version False, and quant_sf_only, False\n",
        )

    @patch("pyrefinebio.script.hlf.create_token")
    def test_create_token_prompt(self, mock_create_token):
        self.runner.invoke(cli, ["create-token"])

        mock_create_token.assert_called_with(None, None)

    @patch("pyrefinebio.script.hlf.create_token")
    def test_create_token_automatic(self, mock_create_token):
        self.runner.invoke(cli, ["create-token", "-s"])

        mock_create_token.assert_called_with(True, True)
