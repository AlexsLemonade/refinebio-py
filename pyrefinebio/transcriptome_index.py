from pyrefinebio import computational_result as prb_computational_result
from pyrefinebio.api_interface import get_by_endpoint
from pyrefinebio.base import Base
from pyrefinebio.util import create_paginated_list, parse_date


class TranscriptomeIndex(Base):
    """Transcriptome Index.

    get a TranscriptomeIndex by id

        >>> import pyrefinebio
        >>> id = 1
        >>> t_index = pyrefinebio.TranscriptomeIndex.get(id)

    Retrieve a list of TranscriptomeIndex based on filters

        >>> import pyrefinebio
        >>> t_indecies = pyrefinebio.TranscriptomeIndex.search(organism_name="GORILLA")
    """

    def __init__(
        self,
        id=None,
        assembly_name=None,
        organism_name=None,
        database_name=None,
        release_version=None,
        index_type=None,
        salmon_version=None,
        download_url=None,
        result_id=None,
        last_modified=None,
    ):
        super().__init__(identifier=id)

        self.id = id
        self.assembly_name = assembly_name
        self.organism_name = organism_name
        self.database_name = database_name
        self.release_version = release_version
        self.index_type = index_type
        self.salmon_version = salmon_version
        self.download_url = download_url
        self.result_id = result_id
        self.result = prb_computational_result.ComputationalResult(id=result_id)
        self.last_modified = parse_date(last_modified)

    @classmethod
    def get(cls, id):
        """Retrieve a TranscriptomeIndex based on id

        Returns:
            TranscriptomeIndex

        Parameters:
            id (int): the id for the TranscriptomeIndex you want to get
        """
        response = get_by_endpoint("transcriptome_indices/" + str(id)).json()
        return TranscriptomeIndex(**response)

    @classmethod
    def search(cls, **kwargs):
        """Retrieve a list of TranscriptomeIndex based on various filters

        Returns:
            list of TranscriptomeIndex

        Keyword Arguments:
            salmon_version (str): filter based on the TranscriptomeIndex's salmon version eg. salmon 0.13.1

            index_type (str): `TRANSCRIPTOME_LONG` or `TRANSCRIPTOME_SHORT`.
                              If the average read length of the RNA-Seq sample you want to process
                              is greater than 75 base pairs, use `TRANSCRIPTOME_LONG` otherwise use
                              `TRANSCRIPTOME_SHORT`

            ordering (str): which field to use when ordering the results.

            limit (int): number of results to return per page.

            offset (int): the initial index from which to return the results.

            organism__name (str): filter based on the name of the Organism associated
                                  with the TranscriptomeIndex

            length (str): short hand for index_type eg. `short` or `long`
                          see `index_type` for more information
        """
        response = get_by_endpoint("transcriptome_indices", params=kwargs)
        return create_paginated_list(cls, response)
