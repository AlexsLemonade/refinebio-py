from pyrefinebio.http import get_by_endpoint
from pyrefinebio.util import generator_from_pagination


class TranscriptomeIndex:
    """Transcriptome Index.

    get a transcriptome index by id

        ex:
        >>> import pyrefinebio
        >>> id = 1
        >>> t_index = pyrefinebio.TranscriptomeIndex.get(id)

    Retrieve a list of transcriptome indecies

        ex:
        >>> import pyrefinebio
        >>> t_indecies = pyrefinebio.TranscriptomeIndex.search(organism_name="GORILLA")
    """

    def __init__(
        self,
        id=None,
        assembly_name=None,
        organism_name=None,
        source_version=None,
        index_type=None,
        salmon_version=None,
        download_url=None,
        result_id=None,
        last_modified=None,
    ):
        self.id = id
        self.assembly_name = assembly_name
        self.organism_name = organism_name
        self.source_version = source_version
        self.index_type = index_type
        self.salmon_version = salmon_version
        self.download_url = download_url
        self.result_id = result_id
        self.last_modified = last_modified

    @classmethod
    def get(cls, id):
        """Retrieve a transcriptome index based on id

        returns: TranscriptomeIndex

        parameters:

            id (int): the id for the transcriptome index you want to get
        """
        response = get_by_endpoint("transhriptome_indices/" + id)
        return TranscriptomeIndex(**response)

    @classmethod
    def search(cls, **kwargs):
        """Retrieve a list of transcriptome indicies based on various filters

        returns: list of TranscriptomeIndex

        parameters:

            salmon_version (str): Eg. salmon 0.13.1

            index_type (str): Eg. TRANSCRIPTOME_LONG

            ordering (str): Which field to use when ordering the results.

            limit (int): Number of results to return per page.

            offset (int): The initial index from which to return the results.

            organism_name (str): Organism name. Eg. MUS_MUSCULUS

            length (str): Short hand for index_type Eg. short or long
        """
        response = get_by_endpoint("transhriptome_indices", params=kwargs)
        return generator_from_pagination(response, cls)
