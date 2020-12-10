from pyrefinebio.http import get_by_endpoint
from pyrefinebio.util import create_paginated_list, parse_date

from pyrefinebio import computational_result as prb_computational_result
from pyrefinebio import sample as prb_sample


class ComputedFile:
    """Computed File.

    ComputedFiles are representation of files created by data-refinery processes.

    Retrieve a ComputedFile based on id

        ex:
        >>> import pyrefinebio
        >>> id = 1
        >>> file = pyrefinebio.ComputedFile.get(id)

    Retrieve a list of ComputedFile based on filters

        ex:
        >>> import pyrefinebio
        >>> files = pyrefinebio.ComputedFile.search(is_compendia=True, is_public=True)
    """

    def __init__(
        self,
        id=None,
        filename=None,
        samples=None,
        size_in_bytes=None,
        is_qn_target=None,
        is_smashable=None,
        is_qc=None,
        is_compendia=None,
        quant_sf_only=None,
        compendia_version=None,
        compendia_organism_name=None,
        sha1=None,
        s3_bucket=None,
        s3_key=None,
        s3_url=None,
        download_url=None,
        created_at=None,
        last_modified=None,
        result=None,
    ):
        self.id = id
        self.filename = filename
        self.samples = [prb_sample.Sample(**sample) for sample in samples] if samples else []
        self.size_in_bytes = size_in_bytes
        self.is_qn_target = is_qn_target
        self.is_smashable = is_smashable
        self.is_qc = is_qc
        self.is_compendia = is_compendia
        self.quant_sf_only = quant_sf_only
        self.compendia_version = compendia_version
        self.compendia_organism_name = compendia_organism_name
        self.sha1 = sha1
        self.s3_bucket = s3_bucket
        self.s3_key = s3_key
        self.s3_url = s3_url
        self.download_url = download_url
        self.created_at = parse_date(created_at)
        self.last_modified = parse_date(last_modified)
        self.result = prb_computational_result.ComputationalResult(**(result)) if result else None

    @classmethod
    def get(cls, id):
        """Retrieve a specific ComputedFile based on id

        Returns:
            ComputedFile

        Parameters:
            id (int): the id for the ComputedFile you want to get
        """
        response = get_by_endpoint("computed_files/" + str(id)).json()
        return ComputedFile(**response)

    @classmethod
    def search(cls, **kwargs):
        """Retrieve a list of a ComputedFiles based on filters

        Returns:
            list of ComputedFile

        Keyword Arguments:

            id (int): filter based on the id of the ComputedFile

            samples (str): filter based on the accession code for Samples related to the ComputedFile

            is_qn_target (bool): filter based on if the ComputedFile is a qn target

            is_smashable (bool): filter based on if the ComputedFile can be added to a normalized
                                 Dataset

            is_qc (bool): filter based on if the ComputedFile contains data about 
                          the quality control of a result rather than data about the
                          result itself

            is_compendia (bool): filter based on if the ComputedFile is part of a compendium

            quant_sf_only (bool): filter based on if the Samples associated with the ComputedFile
                                  are RNA-seq only

            svd_algorithm (str): filter based on the SVD algorithm used for the ComputedFile

            compendia_version (int): filter based on the compendia version of the ComputedFile

            created_at (str): filter based on the time that the ComputedFile was created

            last_modified (str): filter based on the time that the ComputedFile was last modified

            result__id (int): filter based on the id of the ComputationalResult associated with the 
                              ComputedFile

            ordering (str): which field to use when ordering the results

            limit (int): number of results to return per page

            offset (int): the initial index from which to return the results
        """
        response = get_by_endpoint("computed_files", params=kwargs)
        return create_paginated_list(cls, response)
