from pyrefinebio import computed_file as prb_computed_file

from pyrefinebio.http import get_by_endpoint
from pyrefinebio.util import generator_from_pagination


class Compendium:
    """Compendium

    Retrieve a compendium result based on id

        ex:
        >>> import pyrefinebio
        >>> id = 1
        >>> result = pyrefinebio.Compendium.get(id)

    Retrieve a list of compendium results based on filters

        ex:
        >>> import pyrefinebio
        >>> result = pyrefinebio.Compendium.search(primary_organism__name="ACTINIDIA_CHINENSIS")
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
        result = get_by_endpoint("compendia/" + str(id))
        return Compendia(**result)

    @classmethod
    def search(cls, **kwargs):
        """Retrieve a list of compendium results based on filters

        returns: list of Compendia

        valid filters:

            primary_organism__name (str): filter based on the name of the primary
                                          organism associated with the compendium 

            compendium_version (int): filter based on the compendium's version

            quant_sf_only (bool): true for RNA-seq Sample Compendium
                                  results or False for quantile normalized.

            result__id (int): filter based on the id of the result associated with the compendium

            ordering (str): which field to use when ordering the results

            limit (int): number of results to return per page

            offset (int): the initial index from which to return the results

            latest_version (bool): true will only return the highest
                                   compendium_version for each primary_organism.
        """
        result = get_by_endpoint("compendia", params=kwargs)
        return generator_from_pagination(result, cls)
