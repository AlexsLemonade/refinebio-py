import pyrefinebio
import re

from pyrefinebio import Dataset, Compendia
from pyrefinebio.http import download_file
from pyrefinebio.exceptions import DownloadError

def help(entity=None):
    """Help

    Prints out information about pyrefinebio's classes and functions.
    To get information about a class method, pass in the class name and method name  
    separated by either a space or a `.`
    
    usage:

        getting info about classes:

        >>> pyrefinebio.help("Sample")
        
        gettting info about class methods:

        >>> pyrefinebio.help("Sample.get")
        or
        >>> pyrefinebio.help("Sample get")
    """

    if not entity:
        print()
        return

    try:
        final_entity = pyrefinebio
        for attr in re.split("[. ]", entity):
            final_entity = getattr(final_entity, attr)
        print(final_entity.__doc__)
    except:
        print("could not find class or attribute: ", entity)



def download_dataset(
    experiments=None,
    samples=None,
    aggregation="EXPERIMENT",
    transformation="NONE",
    skip_quantile_normalization=False
):
    dataset = Dataset(
        aggregate_by=aggregation,
        quantile_normalize=(not skip_quantile_normalization)
    )

    pass


def download_compendium(
    organism,
    path,
    quant_sf_only=False
):
    compendia = Compendia.search(
        primary_organism__name=organism,
        quant_sf_only=quant_sf_only,
        latest_version=True
    )

    if not compendia:
        raise DownloadError(
            "Compendium", 
            extra_info="Could not find any Compendium with organism name, {0} and quant_sf_only, {1}"
                .format(organism, quant_sf_only)
        )

    download_url = compendia[0].computed_file.download_url

    if not download_url:
        raise DownloadError(
            "Compendium", 
            extra_info="No download url found. Make sure you have an activated api token set up.\n" +
                       "See pyrefinebio.Token for more info"
        )
    
    download_file(download_url, path)


def download_quandfile_compendium(organism, path):
    download_compendium(organism, path, True)
