import click
import json

import pyrefinebio.high_level_functions as hlf 

from pyrefinebio.exceptions import DownloadError

@click.group()
def cli():
    """RefineBio CLI
    """
    pass

class DictParamType(click.ParamType):
    name = "dict"

    def convert(self, value, param, ctx):
        try:
            return json.loads(value)
        except:
            self.fail(
                "expected valid string in a dict form, "
                "got: {0}".format(value),
                param,
                ctx
            )


class ListParamType(click.ParamType):
    name = "list"

    def convert(self, value, param, ctx):
        try:
            return value.split()
        except:
            self.fail(
                "expected valid string in list form, "
                "got: {0}".format(value),
                param,
                ctx
            )


@cli.command()
@click.option("--entity", default="", help="entity to print help for")
def help(entity=None):
    """
    Prints out information about pyrefinebio's classes and functions.
    To get information about a class method, pass in the class name and method name  
    separated by either a space or a `.`

    Example:
        $ refinebio help --entity "Sample.search"
    """
    hlf.help(entity)


@cli.command()
@click.option("--path", required=True, help="Path that the dataset should be downloaded to")
@click.option("--email-address", required=True, help="The email that will be contacted with info related to the Dataset")
@click.option("--dataset-dict", default=None, type=DictParamType(), help="A fully formed Dataset `data` attribute. Use this parameter if you want to specify specific Samples for your Dataset. Ex: '{\"GSE74410\": [\"GSM1919903\"]}' ")
@click.option("--experiments", default=None, type=ListParamType(), help="A space separated list of experiment accession codes. Ex: 'SRP051449 GSE44421 GSE44422'")
@click.option("--aggregation", default="EXPERIMENT", type=click.Choice(("EXPERIMENT", "SPECIES", "ALL"), case_sensitive=True), help="How the Dataset should be aggregated")
@click.option("--transformation", default="NONE", type=click.Choice(("NONE", "MINMAX", "STANDARD"), case_sensitive=True), help="The transformation for the Dataset")
@click.option("--skip-quantile-normalization", default=False, help="Control whether the Dataset should skip quantile normalization for RNA-seq Samples")
def download_dataset(
    path,
    email_address,
    dataset_dict,
    experiments,
    aggregation,
    transformation,
    skip_quantile_normalization
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
            skip_quantile_normalization
        )
    except DownloadError as e:
        raise click.ClickException(e.message)


@cli.command()
@click.option("--path", help="Path that the Compendium should be downloaded to")
@click.option("--organism", help="The name fo the Organism for the Compendium you want to download")
@click.option("--quant-sf-only", default=False, type=click.BOOL, help="True for RNA-seq Sample Compendium results or False for quantile normalized")
def download_compendium(
    path,
    organism,
    quant_sf_only=False
):
    """
    Download a Compendium for the specified organism.
    """
    try:
        hlf.download_compendium(
            path,
            organism,
            quant_sf_only
        )
    except DownloadError as e:
        raise click.ClickException(e.message)


@cli.command()
@click.option("--path", help="Path that the Compendium should be downloaded to")
@click.option("--organism", help="The name fo the Organism for the Compendium you want to download")
def download_quandfile_compendium(path, organism):
    """
    Download a Compendium for the specified organism.
    This command will always download RNA-seq Sample Compedium results.
    """
    try:
        hlf.download_quandfile_compendium(path, organism)
    except DownloadError as e:
        raise click.ClickException(e.message)