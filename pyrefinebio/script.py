import json
from datetime import timedelta

import click
import pyrefinebio.high_level_functions as hlf
import pytimeparse
from pyrefinebio.exceptions import DownloadError


@click.group()
def cli():
    """RefineBio CLI"""
    pass


class JsonParamType(click.ParamType):
    name = "json"

    def convert(self, value, param, ctx):
        try:
            return json.loads(value)
        except:
            self.fail("expected valid json string, got: {0}".format(value), param, ctx)


class ListParamType(click.ParamType):
    name = "list"

    def convert(self, value, param, ctx):
        try:
            return value.split()
        except:
            self.fail("expected valid string in list form, got: {0}".format(value), param, ctx)


class TimedeltaParamType(click.ParamType):
    name = "timedelta"

    def convert(self, value, param, ctx):
        try:
            seconds = pytimeparse.parse(value)
            return timedelta(seconds=seconds)
        except:
            self.fail(
                "expected a string representing a timeout like '5 minutes', got: {0}".format(value),
                param,
                ctx,
            )


@cli.command(no_args_is_help=True)
@click.argument("entity", nargs=1)
def describe(entity=None):
    """
    Prints out information about pyrefinebio's classes and functions.

    ENTITY is the pyrefinebio class or function you want information about.

    To get information about a class method, pass in the class name and method name
    separated by either a space or a `.`

    Example:

    $ refinebio describe "Sample.search"
    """
    hlf.help(entity)


@cli.command()
@click.option(
    "--email-address",
    required=True,
    help="The email that will be contacted with info related to the Dataset",
)
@click.option(
    "--path", default="./", type=click.Path(), help="Path that the dataset should be downloaded to"
)
@click.option(
    "--dataset-dict",
    default=None,
    type=JsonParamType(),
    help=(
        "A fully formed Dataset `data` attribute in JSON format. Use this parameter if you want "
        'to specify specific Samples for your Dataset. Ex: \'{"GSE74410": ["GSM1919903"]}\''
    ),
)
@click.option(
    "--experiments",
    default=None,
    type=ListParamType(),
    help="A space separated list of experiment accession codes. Ex: 'SRP051449 GSE44421 GSE44422'",
)
@click.option(
    "--aggregation",
    default="EXPERIMENT",
    type=click.Choice(("EXPERIMENT", "SPECIES", "ALL"), case_sensitive=True),
    help="How the Dataset should be aggregated",
)
@click.option(
    "--transformation",
    default="NONE",
    type=click.Choice(("NONE", "MINMAX", "STANDARD"), case_sensitive=True),
    help="The transformation for the Dataset",
)
@click.option(
    "--skip-quantile-normalization",
    default=False,
    type=click.BOOL,
    help="Control whether the Dataset should skip quantile normalization for RNA-seq Samples",
)
@click.option(
    "--timeout",
    default=None,
    type=TimedeltaParamType(),
    help="A string representing how long to wait for the dataset to process such as '15 minutes'.",
)
@click.option(
    "--notify-me",
    is_flag=True,
    help="Control whether or not refine.bio should send you an email when your Dataset has finished processing.",
)
def download_dataset(
    email_address,
    path,
    dataset_dict,
    experiments,
    aggregation,
    transformation,
    skip_quantile_normalization,
    timeout,
    notify_me,
):
    """
    Automatically constructs a Dataset, processes it, waits for it
    to finish processing, then downloads it to the path specified.
    """
    try:
        hlf.download_dataset(
            path,
            email_address,
            dataset_dict,
            experiments,
            aggregation,
            transformation,
            skip_quantile_normalization,
            timeout=timeout,
            notify_me=notify_me,
        )
    except DownloadError as e:
        raise click.ClickException(str(e))


@cli.command()
@click.option("--organism", help="The name of the Organism for the Compendium you want to download")
@click.option(
    "--path",
    default="./",
    type=click.Path(),
    help="Path that the Compendium should be downloaded to",
)
@click.option(
    "--quant-sf-only",
    default=False,
    type=click.BOOL,
    help="True for RNA-seq Sample Compendium results or False for quantile normalized",
)
def download_compendium(organism, path, quant_sf_only=False):
    """
    Download a Compendium for the specified organism.
    For more information on normalized Compendia check out the following link:
    http://docs.refine.bio/en/latest/main_text.html#normalized-compendia
    """
    try:
        hlf.download_compendium(path, organism, quant_sf_only)
    except DownloadError as e:
        raise click.ClickException(str(e))


@cli.command()
@click.option("--organism", help="The name of the Organism for the Compendium you want to download")
@click.option(
    "--path",
    default="./",
    type=click.Path(),
    help="Path that the Compendium should be downloaded to",
)
def download_quantfile_compendium(organism, path):
    """
    Download a Compendium for the specified organism.
    This command will always download RNA-seq Sample Compendium results.
    For more information on RNA-seq Sample Compendia check out the following link:
    http://docs.refine.bio/en/latest/main_text.html#rna-seq-sample-compendia
    """
    try:
        hlf.download_quantfile_compendium(path, organism)
    except DownloadError as e:
        raise click.ClickException(e.message)


@cli.command()
@click.option(
    "-s",
    "--silent",
    is_flag=True,
    help="Add this flag if you don't want to be prompted before activating AND saving your token.",
)
def create_token(silent):
    """
    Automatically creates a Token, activates it, and stores it to the Config file.
    The Config file's location is `~/.refinebio.yaml` this file will be created if it
    doesn't exist. For more information see pyrefinbio.Config.
    https://alexslemonade.github.io/refinebio-py/config.html

    By default, will prompt the user before activating and storing the created Token.
    """
    agree_to_terms = silent or None
    save_token = silent or None
    hlf.create_token(agree_to_terms, save_token)
