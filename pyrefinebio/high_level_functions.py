import pyrefinebio
import re
import time

from pyrefinebio import Dataset, Compendium
from pyrefinebio.http import download_file
from pyrefinebio.exceptions import DownloadError

def help(entity=None):
    """Help

    Prints out information about pyrefinebio's classes and functions.
    To get information about a class method, pass in the class name and method name  
    separated by either a space or a `.`
    
    Examples:
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
    email_address,
    dataset_dict=None,
    experiments=None,
    aggregation="EXPERIMENT",
    transformation="NONE",
    skip_quantile_normalization=False
):
    """download_dataset

        Automatically constructs a Dataset, processes it, waits for it
        to finish processing, then downloads it to the path specified.

        Returns:
            void

        Parameters:
            path (str): the path that the Dataset should be downloaded to

            email_address (str): the email address that will be contacted with info
                                 related to the dataset
            
            dataset_dict (dict): a fully formed Dataset `data` attribute in the form:
                                 {
                                     "Experiment": [
                                         "Sample",
                                         "Sample"
                                     ]
                                 }
                                 use this parameter if you want to specify specific Samples
                                 for your dataset
                                 each part of the dict can be a pyrefinebio object or an accession
                                 code as a string

            experiments (list): a list of Experiments that should be added to the dataset
                                use this parameter if you only care about the Experiments - all 
                                available samples related to each Experiment will be added  
                                the list can contain Experiment objects or accession codes as strings

            aggregation (str): how the Dataset should be aggregated - by `EXPERIMENT` or by `SPECIES`

            transformation (str): the transformation for the dataset - `NONE`, `MINMAX`, or `STANDARD`

            skip_quantile_normalization (bool): control whether or not the dataset should skip quantile
                                                normalization for RNA-seq Samples
    """
    if dataset_dict and experiments:
        raise DownloadError(
            "Dataset", 
            extra_info="You should either provide dataset_dict or experiments but not both"
        )

    dataset = Dataset(
        email_address=email_address,
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

    Returns:
        void

    Parameters:
        path (str): the path that the Compendium should be downloaded to

        organism (str): the name of the Organism for the Compendium you want to 
                        download

        quant_sf_only (bool): true for RNA-seq Sample Compendium results or False 
                              for quantile normalized.

    """
    compendium = Compendium.search(
        primary_organism__name=organism,
        quant_sf_only=quant_sf_only,
        latest_version=True
    )

    if not compendium:
        raise DownloadError(
            "Compendium", 
            extra_info="Could not find any Compendium with organism name, {0} and quant_sf_only, {1}"
                .format(organism, quant_sf_only)
        )

    download_url = compendium[0].computed_file.download_url

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

    Returns:
        void

    Parameters:
        path (str): the path that the Compendium should be downloaded to 

        organism (str): the name of the Organism for the Compendium you want to 
                        download
    """
    download_compendium(organism, path, True)
