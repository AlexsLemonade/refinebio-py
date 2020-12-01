from pyrefinebio.http import get_by_endpoint
from pyrefinebio.util import create_paginated_list


class Organism:
    """Organism.

    Retrieve an Organism by name

        ex:
        >>> import pyrefinebio
        >>> name = "GORILLA"
        >>> organism = pyrefinebio.Organism.get(name)

    Retrieve a list of Organisms

        ex:
        >>> import pyrefinebio
        >>> organisms = pyrefinebio.Organism.search()
    """

    def __init__(
        self,
        name=None,
        taxonomy_id=None
    ):
        self.name = name
        self.taxonomy_id = taxonomy_id

    @classmethod
    def get(cls, name):
        """Retrieve an Organism based on name

        returns: Organism

        parameters:

            name (str): the name for the Organism you want to get
        """

        response = get_by_endpoint("organisms/" + name).json()
        return Organism(**response)

    @classmethod
    def search(cls, **kwargs):
        """Retrieve a list of Organisms

        returns: list of Organism

        Since there are no filters, this method always returns all organisms
        """
        response = get_by_endpoint("organisms", params=kwargs)
        return create_paginated_list(cls, response)
