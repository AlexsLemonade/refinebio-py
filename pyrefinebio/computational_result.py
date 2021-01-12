from pyrefinebio.http import get_by_endpoint
from pyrefinebio.util import create_paginated_list, parse_date

from pyrefinebio.common import annotation as prb_annotation
from pyrefinebio import transcriptome_index as prb_transcriptome_index
from pyrefinebio import computed_file as prb_computed_file
from pyrefinebio import processor as prb_processor


class ComputationalResult:
    """Computational Result

    Retrieve a ComputationalResult based on id

        >>> import pyrefinebio
        >>> id = 1
        >>> result = pyrefinebio.ComputationalResult.get(id)

    Retrieve a list of ComputationalResult based on filters

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
        self.annotations = (
            [prb_annotation.Annotation(**annotation) for annotation in annotations]
            if annotations
            else []
        )
        self.files = [prb_computed_file.ComputedFile(**file) for file in files] if files else []
        self.organism_index = (
            prb_transcriptome_index.TranscriptomeIndex(**(organism_index)) if organism_index else None
        )
        self.time_start = parse_date(time_start)
        self.time_end = parse_date(time_end)
        self.created_at = parse_date(created_at)
        self.last_modified = parse_date(last_modified)

    @classmethod
    def get(cls, id):
        """Retrieve a computational result based on its id.

        Returns:
            ComputationalResult

        Parameters:
            id (int): The id for the computational result to be retrieved.
        """
        response = get_by_endpoint("computational_results/" + str(id)).json()
        return ComputationalResult(**response)

    @classmethod
    def search(cls, **kwargs):
        """Retrieve a list of computational results based on filters.

        Returns:
            list of ComputationalResult

        Keyword Arguments:
            processor__id (int): id of the Processor that processed the result

            limit (int): number of results to return per page

            offset (int): the initial index from which to return the results
        """
        response = get_by_endpoint("computational_results", params=kwargs)
        return create_paginated_list(cls, response)
