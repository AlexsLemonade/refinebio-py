import re
import time
from datetime import datetime, timedelta

import pyrefinebio
from pyrefinebio import Compendium, Dataset, Token
from pyrefinebio.exceptions import DownloadError


def help(entity=None):
    """Help

    Prints out information about pyrefinebio's classes and functions.
    To get information about a class method, pass in the class name and method name
    separated by either a space or a `.`

    Examples:
        getting information about classes:

        >>> pyrefinebio.help("Sample")

        getting information about class methods:

        >>> pyrefinebio.help("Sample.get")
        or
        >>> pyrefinebio.help("Sample get")

        getting information about functions:

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
    skip_quantile_normalization=False,
    quant_sf_only=False,
    timeout=None,
    extract=False,
    prompt=True,
    notify_me=False,
):
    """download_dataset

    Automatically constructs a Dataset, processes it, waits for it
    to finish processing, then downloads it to the path specified.

    Returns:
        Dataset

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

        aggregation (str): how the Dataset should be aggregated - by `EXPERIMENT`, by `SPECIES`, or by `ALL`

        transformation (str): the transformation for the dataset - `NONE`, `MINMAX`, or `STANDARD`

        skip_quantile_normalization (bool): control whether or not the dataset should skip quantile
                                            normalization for RNA-seq Samples

        quant_sf_only (bool): include only quant.sf files in the generated dataset.

        timeout (datetime.timedelta): if specified the function will return None after timeout is reached.

        extract (bool): if true, the downloaded zip file will be automatically extracted

        prompt (bool): if true, will prompt before downloading files bigger than 1GB

        notify_me (bool): if true, refine.bio will send you an email when the dataset has finished processing.
                          Defaults to False.
    """
    if dataset_dict and experiments:
        raise DownloadError(
            "Dataset",
            extra_info="You should either provide dataset_dict or experiments but not both",
        )

    print("Creating Dataset...")

    dataset = Dataset(
        email_address=email_address,
        aggregate_by=aggregation,
        quantile_normalize=(not skip_quantile_normalization),
        quant_sf_only=quant_sf_only,
        notify_me=notify_me,
    )

    if dataset_dict:
        dataset.data = dataset_dict

    if experiments:
        for experiment in experiments:
            dataset.add_samples(experiment)

    print("Processing Dataset...")

    dataset.process()

    start_time = datetime.now()
    while not dataset.check():
        if not dataset.is_processing and not dataset.is_processed:
            print(
                "Dataset failed to process. The system may be experiencing issues."
                " Please try again later."
            )
            return None
        elif timeout and datetime.now() - start_time > timeout:
            print(
                (
                    "Dataset not processed after {0}. The system may be experiencing issues"
                    " or your dataset may just be taking a while to process. You can check on its"
                    " progress at https://refine.bio/dataset/{1}"
                ).format(timeout, dataset.id)
            )
            return None

        time.sleep(5)

    print("Downloading Dataset...")

    dataset = dataset.download(path, prompt)

    if extract:
        print("Extracting Dataset...")
        dataset.extract()

    return dataset


def download_compendium(
    path, organism, version=None, quant_sf_only=False, extract=False, prompt=True
):
    """download_compendium

    Download a Compendium for the specified organism.

    Returns:
        Compendium

    Parameters:
        path (str): the path that the Compendium should be downloaded to

        organism (str): the name of the Organism for the Compendium you want to
                        download

        version (int): the version for the Compendium you want to download - None
                       for latest version

        quant_sf_only (bool): true for RNA-seq Sample Compendium results or False
                              for quantile normalized

        extract (bool): if true, the downloaded zip file will be automatically extracted

        prompt (bool): if true, will prompt before downloading files bigger than 1GB
    """
    search_params = {"primary_organism__name": organism, "quant_sf_only": quant_sf_only}

    if version:
        search_params["compendium_version"] = version
    else:
        search_params["latest_version"] = True

    print("Searching for Compendium...")

    compendium = Compendium.search(**search_params)

    if not compendium:
        raise DownloadError(
            "Compendium",
            extra_info="Could not find any Compendium with organism name, {0}, version {1}, and quant_sf_only, {2}".format(
                organism, version, quant_sf_only
            ),
        )

    print("Downloading Compendium...")

    compendium = compendium[0].download(path, prompt)

    if extract:
        print("Extracting Compendium...")
        compendium.extract()

    return compendium


def download_quantfile_compendium(path, organism, version=None, extract=False, prompt=True):
    """download_quantfile_compendium

    Download a Compendium for the specified organism.
    This function will always download RNA-seq Sample Compedium results.

    Returns:
        Compendium

    Parameters:
        path (str): the path that the Compendium should be downloaded to

        organism (str): the name of the Organism for the Compendium you want to
                        download

        version (int): the version for the Compendium you want to download - None
                       for latest version

        extract (bool): if true, the downloaded zip file will be automatically extracted

        prompt (bool): if true, will prompt before downloading files bigger than 1GB
    """
    return download_compendium(
        path, organism, version=version, quant_sf_only=True, extract=extract, prompt=prompt
    )


def create_token(agree_to_terms=None, save_token=None):
    """create_token

    Automatically creates a Token, activates it, and stores it to the Config file.

    By default, will prompt the user before activating and storing the created Token.

    Returns:
        Token

    Parameters:
        agree_to_terms (bool): if true, the token will be automatically activated without prompting.
                               If false, the token will not be activated. Leave as None to be prompted
                               before activating.

        save_token (bool): if true, the token will be automatically saved. If false, the token will
                           not be saved. Leave as None to be prompted before saving.
    """
    if agree_to_terms is None:
        print(
            "Please review the refine.bio Terms of Use: https://www.refine.bio/terms and Privacy Policy: https://www.refine.bio/privacy"
        )
        yn = input("Do you understand and accept both documents? (y/N)")
        agree_to_terms = yn.lower() in ("y", "yes")

    token = Token()

    if agree_to_terms:
        token.agree_to_terms_and_conditions()

    if save_token is None:
        yn = input("Would you like to save your Token to the Config file for future use? (y/N)")
        save_token = yn.lower() in ("y", "yes")

    if save_token:
        token.save_token()

    return token
