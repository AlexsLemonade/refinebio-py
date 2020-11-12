from pyrefinebio import computed_file as prb_computed_file

from pyrefinebio.http import get_by_endpoint
from pyrefinebio.util import create_paginated_list


class Compendia:
    """Compendia

    Retrieve a compendium result based on id

        ex:
        >>> import pyrefinebio
        >>> id = 1
        >>> sample = pyrefinebio.Compendia.get(id)

    Retrieve a list of compendium results based on filters

        ex:
        >>> import pyrefinebio
        >>> samples = pyrefinebio.Compendia.search(compendium_version="")
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
        self.id = id
        self.primary_organism_name = primary_organism_name
        self.organism_names = organism_names
        self.svd_algorithm = svd_algorithm
        self.quant_sf_only = quant_sf_only
        self.compendium_version = compendium_version
        self.computed_file = (
            prb_computed_file.ComputedFile(**(computed_file)) if computed_file else None
        )

    @classmethod
    def get(cls, id):
        """Retrieve a specific compendium result based on id

        returns: Compendia

        parameters:

            id (int): the id for the compendium result you want to get
        """
        response = get_by_endpoint("compendia/" + str(id)).json()
        return Compendia(**response)

    @classmethod
    def search(cls, **kwargs):
        """Retrieve a list of compendium results based on filters

        returns: list of Compendia

        parameters:

            primary_organism__name (str):

            compendium_version (int):

            quant_sf_only (bool): True for RNA-seq Sample Compendium
                                  results or False for quantile normalized.

            result__id (int):

            ordering (str): Which field to use when ordering the results.

            limit (int): Number of results to return per page.

            offset (int): The initial index from which to return the results.

            latest_version (bool): True will only return the highest
                                   compendium_version for each primary_organism.
        """
        response = get_by_endpoint("compendia", params=kwargs)
        return create_paginated_list(cls, response)
