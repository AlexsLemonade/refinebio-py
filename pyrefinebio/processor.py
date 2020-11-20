from pyrefinebio.http import get_by_endpoint
from pyrefinebio.util import create_paginated_list


class Processor:
    """Processor.

    Retrieve a processor by id

        ex:
        >>> import pyrefinebio
        >>> id = 1
        >>> processor = pyrefinebio.Processor.get(id)

    Retrieve a list of processors

        ex:
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
        """Retrieve a processor based on id

        returns: Processor

        parameters:

            id (int): the id for the processor you want to get
        """
        response = get_by_endpoint("processors/" + str(id)).json()
        return Processor(**response)

    @classmethod
    def search(cls, **kwargs):
        """Retrieve a list of processors

        returns: list of Processor

        Since there are no filters, this method always returns all processors
        """
        response = get_by_endpoint("processors", params=kwargs)
        return create_paginated_list(cls, response)
