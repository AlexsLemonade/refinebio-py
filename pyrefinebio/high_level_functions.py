import pyrefinebio
import re
import time

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

        getting info about functions:

        >>> pyrefinebio.help("download_dataset")
    """

    if not entity:
        print(help.__doc__)
        return

    try:
        final_entity = pyrefinebio
        for attr in re.split("[. ]", entity):
            final_entity = getattr(final_entity, attr)
        print(final_entity.__doc__)
    except:
        print("could not find class or attribute: ", entity)



def download_dataset(
    path,
    dataset_dict=None,
    experiments=None,
    aggregation="EXPERIMENT",
    transformation="NONE",
    skip_quantile_normalization=False
):
    """download_dataset

        Automatically constructs a Dataset, processes it, waits for it
        to finish processing, then downloads it to the path specified.

        returns: void

        parameters:

            path (str):
            
            dataset_dict (dict):

            experiments (list):

            aggregation (str):

            transformation (str):

            skip_quantile_normalization (bool):
    """
    if dataset_dict and experiments:
        raise DownloadError(
            "Dataset", 
            extra_info="You should either provide dataset_dict or experiments but not both"
        )

    dataset = Dataset(
        aggregate_by=aggregation,
        quantile_normalize=(not skip_quantile_normalization)
    )

    if dataset_dict:
        dataset.data = dataset_dict
    
    if experiments:
        for experiment in experiments:
            dataset.add_samples(experiment)
    
    dataset.process()

    while not dataset.check():
        time.sleep(5)

    dataset.download(path)


def download_compendium(
    path,
    organism,
    quant_sf_only=False
):
    """download_compendium

    Download a Compendium for the specified organism.

    returns: void

    parameters:

        path (str)

        organism (str):

        quant_sf_only (bool):

    """
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


def download_quandfile_compendium(path, organism):
    """download_quandfile_compendium

    Download a Compendium for the specified organism.
    This function will always download RNA-seq Sample Compedium results.

    returns: void

    parameters:

        path (str):

        organism (str): the name of the Organism 
    """
    download_compendium(organism, path, True)
