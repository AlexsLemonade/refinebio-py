from pyrefinebio import annotation as prb_annotation, sample as prb_sample
from pyrefinebio.api_interface import get_by_endpoint
from pyrefinebio.base import Base
from pyrefinebio.util import create_paginated_list, parse_date


class Experiment(Base):
    """Experiment

    Retrieve an Experiment based on id

        >>> import pyrefinebio
        >>> accession_code = 1
        >>> experiment = pyrefinebio.Experiment.get(accession_code)

    Search for Experiments based on filters

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
        downloadable_organism_names=None,
        sample_metadata_fields=None,
        sample_metadata=None,
        num_total_samples=None,
        num_processed_samples=None,
        num_downloadable_samples=None,
    ):
        super().__init__(identifier=accession_code)

        self.id = id
        self.title = title
        self.description = description
        self.technology = technology
        self.annotations = (
            [prb_annotation.Annotation(**a) for a in annotations] if annotations else []
        )
        self.samples = [prb_sample.Sample(**sample) for sample in samples] if samples else []
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
        self.source_first_published = parse_date(source_first_published)
        self.source_last_modified = parse_date(source_last_modified)
        self.submitter_institution = submitter_institution
        self.platform_names = platform_names
        self.platform_accession_codes = platform_accession_codes
        self.last_modified = parse_date(last_modified)
        self.created_at = parse_date(created_at)
        self.organism_names = organism_names
        self.downloadable_organism_names = downloadable_organism_names
        self.sample_metadata_fields = sample_metadata_fields
        self.sample_metadata = sample_metadata
        self.num_total_samples = num_total_samples
        self.num_processed_samples = num_processed_samples
        self.num_downloadable_samples = num_downloadable_samples

    @classmethod
    def get(cls, accession_code):
        """Retrieve an Experiment based on accession code

        Returns:
            Experiment

        Parameters:
            accession code (str): the accession code for the Experiment you want to get
        """
        response = get_by_endpoint("experiments/" + accession_code).json()
        return Experiment(**response)

    @classmethod
    def search(cls, **kwargs):
        """Search for Experiments based on various filters

        Returns:
            list of Experiment

        Keyword Arguments:
            id (int): filter based on the id of the Experiment

            technology (str): filter based on the technology used for the Experiment
                              (microarray, rna-seq, etc) this filter can have multiple values.

            has_publication (bool): filter based on if the Experiment has associated publications

            accession_code (str): filter based on the Experiment's accession code
                                  this filter can have multiple values

            alternate_accession_code (str): filter based on the Experiment's alternate
                                            accession codes

            platform (str): filter based on  platform, this filter can have multiple values

            organism (str): filter based on Organism, this filter can have multiple values

            downloadable_organism (str): filter based on Organisms that have downloadable files,
                                         this filter can have multiple values

            num_processed_samples (number): filter based on the Experiment's number of processed samples

            num_downloadable_samples (int): filter based on the Experiment's number of downloadable samples

            sample_keywords (str): filter based on keywords associated with the Experiment's Samples

            ordering (str): which field from to use when ordering the results

            search (str): specify a keyword which will be applied to the Experiment's title, publication_authors,
                          sample_keywords, publication_title, submitter_institution, description, accession_code,
                          alternate_accession_code, publication_doi, pubmed_id, sample_metadata_fields, and
                          platform_names

            limit (int): number of results to return per page

            offset (int): the initial index from which to return the results
        """
        response = get_by_endpoint("search", params=kwargs)
        return create_paginated_list(cls, response)
