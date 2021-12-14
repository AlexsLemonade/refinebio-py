import shutil

from pyrefinebio import computed_file as prb_computed_file
from pyrefinebio.api_interface import download_file, get_by_endpoint
from pyrefinebio.base import Base
from pyrefinebio.exceptions import DownloadError, MissingFile
from pyrefinebio.util import create_paginated_list, expand_path


class Compendium(Base):
    """Compendium

    Retrieve a Compendium based on id

        >>> import pyrefinebio
        >>> id = 1
        >>> result = pyrefinebio.Compendium.get(id)

    Retrieve a list of Compendia based on filters

        >>> import pyrefinebio
        >>> results = pyrefinebio.Compendium.search(primary_organism__name="ACTINIDIA_CHINENSIS")
    """

    def __init__(
        self,
        id=None,
        primary_organism_name=None,
        organism_names=None,
        svd_algorithm=None,
        quant_sf_only=None,
        compendium_version=None,
        computed_file=None,
    ):
        super().__init__(identifier=id)

        self.id = id
        self.primary_organism_name = primary_organism_name
        self.organism_names = organism_names
        self.svd_algorithm = svd_algorithm
        self.quant_sf_only = quant_sf_only
        self.compendium_version = compendium_version
        self.computed_file = (
            prb_computed_file.ComputedFile(**(computed_file)) if computed_file else None
        )

        self._downloaded_path = None

    @classmethod
    def get(cls, id):
        """Retrieve a specific Compendium based on id

        Returns:
            Compendium

        Parameters:
            id (int): the id for the Compendium you want to get
        """
        response = get_by_endpoint("compendia/" + str(id)).json()
        return Compendium(**response)

    @classmethod
    def search(cls, **kwargs):
        """Retrieve a list of Compendium results based on filters

        Returns:
            list of Compendium

        Keyword Arguments:
            primary_organism__name (str): filter based on the name of the primary Organism
                                          associated with the compendium

            compendium_version (int): filter based on the Compendium's version

            quant_sf_only (bool): true for RNA-seq Sample Compendium results or False
                                  for quantile normalized

            result__id (int): filter based on the id of the ComputationalResult associated
                              with the compendium

            ordering (str): which field to use when ordering the results

            limit (int): number of results to return per page

            offset (int): the initial index from which to return the results

            latest_version (bool): true will only return the highest
                                   compendium_version for each primary_organism
        """
        response = get_by_endpoint("compendia", params=kwargs)
        return create_paginated_list(cls, response)

    def download(self, path, prompt=True):
        """Download a Compendium result

        Returns:
            Compendium

        Parameters:
            path (str): the path that the Compendium result should be downloaded to

            prompt (bool): if true, will prompt before downloading files bigger than 1GB
        """
        if not self.computed_file.download_url:
            raise DownloadError(
                "Compendia",
                "Download url not found - make sure you have set up and activated your Token. "
                "You can create and activate a new token using pyrefinebio.create_token(). "
                "See documentation for advanced usage: https://alexslemonade.github.io/refinebio-py/token.html",
            )

        full_path = expand_path(path, "compendium-" + str(self.id) + ".zip")

        download_file(self.computed_file.download_url, full_path, prompt)

        self._downloaded_path = full_path

        return self

    def extract(self):
        """Extract a downloaded Compendium

        Returns:
            Compendium
        """
        if not self._downloaded_path:
            raise MissingFile(
                "Compendium downloaded file",
                "Make sure you have successfully downloaded the Compendium before extracting.",
            )

        shutil.unpack_archive(self._downloaded_path)
        return self
