from pyrefinebio.http import get_by_endpoint
from pyrefinebio.util import generator_from_pagination

import pyrefinebio.common.annotation as prb_annotation
import pyrefinebio.common.organism_index as prb_organism_index
import pyrefinebio.computational_result as prb_computational_result
import pyrefinebio.processor as prb_processor
import pyrefinebio.sample as prb_sample


class ComputedFile:
    """Computed File.

    ComputedFiles are representation of files created by data-refinery processes.

    Retrieve a computed file based on id

        ex:
        >>> import pyrefinebio
        >>> id = 1
        >>> file = pyrefinebio.ComputedFile.get(id)

    Retrieve a list of computed files based on filters

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
        self.created_at = created_at
        self.last_modified = last_modified
        self.result = prb_computational_result.ComputationalResult(**(result)) if result else None

    @classmethod
    def get(cls, id):
        """Retrieve a specific computed file based on id

        returns: ComputedFile

        parameters:

            id (int): the id for the computed file you want to get
        """
        response = get_by_endpoint("computed_files/" + str(id))
        return ComputedFile(**response)

    @classmethod
    def search(cls, **kwargs):
        """Retrieve a list of a compendium result based on filters

        returns: list of ComputedFile

        parameters:

            id (int):

            samples (str):

            is_qn_target (bool):

            is_smashable (bool):

            is_qc (bool):

            is_compendia (bool):

            quant_sf_only (true):

            svd_algorithm (str):

            compendia_version (int):

            created_at (str):

            last_modified (str):

            result__id (int):

            ordering (str): Which field to use when ordering the results.

            limit (int): Number of results to return per page.

            offset (int): The initial index from which to return the results.
        """
        result = get_by_endpoint("computed_files", params=kwargs)
        return generator_from_pagination(result, cls)
