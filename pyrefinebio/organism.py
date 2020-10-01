from pyrefinebio.http import get_by_endpoint
from pyrefinebio.util import generator_from_pagination


class Organism:
    """Organism.

    get an organism by name

        ex:
        >>> import pyrefinebio
        >>> name = "GORILLA"
        >>> job = pyrefinebio.Organism.get(name)

    search for an organism based on filters

        ex:
        >>> import pyrefinebio
        >>> jobs = pyrefinebio.Organism.search()
    """

    def __init__(self, name=None, taxonomy_id=None):
        self.name = name
        self.taxonomy_id = taxonomy_id

    @classmethod
    def get(cls, name):
        """Retrieve an organism based on name

        returns: Organism

        parameters:

            name (str): the name for the organism you want to get
        """

        response = get_by_endpoint("organisms/" + name)
        return Organism(**response)

    @classmethod
    def search(cls, **kwargs):
        """Retrieve a list of organisms

        returns: list of Organism

        parameters:
        """
        response = get_by_endpoint("organisms", params=kwargs)
        return generator_from_pagination(response, cls)
