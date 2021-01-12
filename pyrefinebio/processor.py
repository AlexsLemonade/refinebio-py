from pyrefinebio.http import get_by_endpoint
from pyrefinebio.util import create_paginated_list


class Processor:
    """Processor.

    Retrieve a Processor by id

        >>> import pyrefinebio
        >>> id = 1
        >>> processor = pyrefinebio.Processor.get(id)

    Retrieve a list of Processors

        >>> import pyrefinebio
        >>> processors = pyrefinebio.Processor.search()
    """
    def __init__(
        self,
        id=None,
        name=None,
        version=None,
        docker_image=None,
        environment=None
    ):
        self.id = id
        self.name = name
        self.version = version
        self.docker_image = docker_image
        self.environment = environment

    @classmethod
    def get(cls, id):
        """Retrieve a Processor based on id

        Returns:
            Processor

        Parameters:
            id (int): the id for the Processor you want to get
        """
        response = get_by_endpoint("processors/" + str(id)).json()
        return Processor(**response)

    @classmethod
    def search(cls, **kwargs):
        """Retrieve a list of Processors

        Returns:
            list of Processor

        Since there are no filters, this method always returns all Processors
        """
        response = get_by_endpoint("processors", params=kwargs)
        return create_paginated_list(cls, response)
