from pyrefinebio.http import get_by_endpoint
from pyrefinebio.util import generator_from_pagination

import pyrefinebio.common.annotation as prb_annotation
import pyrefinebio.common.organism_index as prb_organism_index
import pyrefinebio.computed_file as prb_computed_file
import pyrefinebio.processor as prb_processor


class ComputationalResult:
    """Computational Result 

    Retrieve a computational result based on id

        ex:
        >>> import pyrefinebio
        >>> id = 1
        >>> result = pyrefinebio.ComputationalResult.get(id)

    Retrieve a list of computational results based on filters

        ex:
        >>> import pyrefinebio
        >>> results = pyrefinebio.ComputationalResult.search(processor_id=4)
    """

    def __init__(
        self,
        id=None,
        commands=None,
        processor=None,
        is_ccdl=None,
        annotations=None,
        files=None,
        organism_index=None,
        time_start=None,
        time_end=None,
        created_at=None,
        last_modified=None,
    ):
        self.id = id
        self.commands = commands
        self.processor = prb_processor.Processor(**(processor)) if processor else None
        self.is_ccdl = is_ccdl
        self.annotations = [prb_annotation.Annotation(**annotation) for annotation in annotations] if annotations else []
        self.files = [prb_computed_file.ComputedFile(**file) for file in files] if files else []
        self.organism_index = prb_organism_index.OrganismIndex(**(organism_index)) if organism_index else None
        self.time_start = time_start
        self.time_end = time_end
        self.created_at = created_at
        self.last_modified = last_modified

    @classmethod
    def get(cls, id):
        """Retrieve a computational result based on its id.

        returns: ComputationalResult

        parameters:

            id (int): The id for the computational result to be retrieved.
        """
        result = get_by_endpoint("computational_results/" + str(id))
        return ComputationalResult(**result)

    @classmethod
    def search(cls, **kwargs):
        """Retrieve a list of computational results based on filters.

        returns: list of ComputationalResult

        parameters:

            processor_id (int): 

            limit (int): Number of results to return per page.

            offset (int): The initial index from which to return the results.
        """
        result = get_by_endpoint("computational_results", params=kwargs)
        return generator_from_pagination(result, cls)
