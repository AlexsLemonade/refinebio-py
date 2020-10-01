from pyrefinebio.http import get_by_endpoint
from pyrefinebio.util import generator_from_pagination


class Processor:
    """Processor.

    get a processor by id

        ex:
        >>> import pyrefinebio
        >>> id = 1
        >>> processor = pyrefinebio.Processor.get(id)

    search for an organism based on filters

        ex:
        >>> import pyrefinebio
        >>> processors = pyrefinebio.Processor.search()
    """
    def __init__(self, id=None, name=None, version=None, docker_image=None, environment=None):
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
        response = get_by_endpoint("processors/" + str(id))
        return Processor(**response)

    @classmethod
    def search(cls, **kwargs):
        """Retrieve a list of processors

        returns: list of Processor
        """
        response = get_by_endpoint("processors", params=kwargs)
        return generator_from_pagination(response, cls)
