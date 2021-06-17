from pyrefinebio.api_interface import get_by_endpoint
from pyrefinebio.base import Base
from pyrefinebio.util import create_paginated_list


class Organism(Base):
    """Organism.

    Retrieve an Organism by name

        >>> import pyrefinebio
        >>> name = "GORILLA"
        >>> organism = pyrefinebio.Organism.get(name)

    Retrieve a list of Organisms

        >>> import pyrefinebio
        >>> organisms = pyrefinebio.Organism.search(has_compendia=True)
    """

    def __init__(
        self, name=None, taxonomy_id=None, has_compendia=None, has_quantfile_compendia=None
    ):
        super().__init__(identifier=name)

        self.name = name
        self.taxonomy_id = taxonomy_id
        self.has_compendia = has_compendia
        self.has_quantfile_compendia = has_quantfile_compendia

    @classmethod
    def get(cls, name):
        """Retrieve an Organism based on name

        Returns:
            Organism

        Parameters:
            name (str): the name for the Organism you want to get
        """

        response = get_by_endpoint("organisms/" + name).json()
        return Organism(**response)

    @classmethod
    def search(cls, **kwargs):
        """Retrieve a list of Organisms based on filters

        Returns:
            list of Organism

        Keyword Arguments:
            has_compendia (bool): filter based on if this Organism has a normalized Compendium
                                  associated with it

            has_quantfile_compendia (bool): filter based on if this Organism has an
                                            RNA-seq Sample Compendium associated with it
        """
        response = get_by_endpoint("organisms", params=kwargs)
        return create_paginated_list(cls, response)
