from pyrefinebio.http import get_by_endpoint
from pyrefinebio.util import generator_from_pagination

from pyrefinebio.common import annotation as prb_annotation
from pyrefinebio import sample as prb_sample


class Experiment:
    """Experiment

    Retrieve an experiment based on id

        ex:
        >>> import pyrefinebio
        >>> accession_code = 1
        >>> experiment = pyrefinebio.Experiment.get(accession_code)

    Search for experiments based on filters

        ex:
        >>> import pyrefinebio
        >>> experiments = pyrefinebio.Experiment.search(is_compendia=True, is_public=True)
    """

    def __init__(
        self,
        id=None,
        title=None,
        description=None,
        technology=None,
        annotations=None,
        samples=None,
        protocol_description=None,
        accession_code=None,
        alternate_accession_code=None,
        source_database=None,
        source_url=None,
        has_publication=None,
        publication_title=None,
        publication_doi=None,
        publication_authors=None,
        pubmed_id=None,
        source_first_published=None,
        source_last_modified=None,
        submitter_institution=None,
        platform_names=None,
        platform_accession_codes=None,
        last_modified=None,
        created_at=None,
        organism_names=None,
        sample_metadata_fields=None,
        sample_metadata=None,
        num_total_samples=None,
        num_processed_samples=None,
        num_downloadable_samples=None,
    ):
        self.id = id
        self.title = title
        self.description = description
        self.technology = technology
        self.annotations = (
            [prb_annotation.Annotation(**a) for a in annotations] if annotations else []
        )
        self.samples = [prb_sample.Sample(**sample) for sample in samples] if annotations else []
        self.protocol_description = protocol_description
        self.accession_code = accession_code
        self.alternate_accession_code = alternate_accession_code
        self.source_database = source_database
        self.source_url = source_url
        self.has_publication = has_publication
        self.publication_title = publication_title
        self.publication_doi = publication_doi
        self.publication_authors = publication_authors
        self.pubmed_id = pubmed_id
        self.source_first_published = source_first_published
        self.source_last_modified = source_last_modified
        self.submitter_institution = submitter_institution
        self.platform_names = platform_names
        self.platform_accession_codes = platform_accession_codes
        self.last_modified = last_modified
        self.created_at = created_at
        self.organism_names = organism_names
        self.sample_metadata_fields = sample_metadata_fields
        self.sample_metadata = sample_metadata
        self.num_total_samples = num_total_samples
        self.num_processed_samples = num_processed_samples
        self.num_downloadable_samples = num_downloadable_samples

    @classmethod
    def get(cls, accession_code):
        """Retrieve an experiment based on accession code

        returns: Experiment

        parameters:

            accession code (str): the accession code for the experiment you want to get
        """
        response = get_by_endpoint("experiments/" + accession_code)
        return Experiment(**response)

    @classmethod
    def search(cls, **kwargs):
        """Search for experiments based on various filters

        returns: list of Experiment

        parameters:

            id (int):

            technology (str): Allows filtering the results by technology, can have multiple values. Eg: ?technology=microarray&technology=rna-seq

            has_publication (bool): Filter the results that have associated publications with ?has_publication=true

            accession_code (str): Allows filtering the results by accession code, can have multiple values. Eg: ?accession_code=microarray&accession_code=rna-seq

            alternate_accession_code (str):

            platform (str): Allows filtering the results by platform, this parameter can have multiple values.

            organism (str): Allows filtering the results by organism, this parameter can have multiple values.

            num_processed_samples (number): Use ElasticSearch queries to specify the number of processed samples of the results

            num_downloadable_samples (int):

            sample_keywords (str):

            ordering (str): Which field from to use when ordering the results.

            search (str): Search in title, publication_authors, sample_keywords, publication_title, submitter_institution, description, accession_code, alternate_accession_code, publication_doi, pubmed_id, sample_metadata_fields, platform_names.

            limit (int): Number of results to return per page.

            offset (int): The initial index from which to return the results.
        """
        response = get_by_endpoint("search", params=kwargs)
        return generator_from_pagination(response, cls)
