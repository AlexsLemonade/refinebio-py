from pyrefinebio import (
    annotation as prb_annotation,
    computational_result as prb_computational_result,
    computed_file as prb_computed_file,
    experiment as prb_experiment,
    organism as prb_organism,
    original_file as prb_original_file,
    job as prb_job,
)
from pyrefinebio.api_interface import get_by_endpoint
from pyrefinebio.base import Base
from pyrefinebio.util import create_paginated_list, parse_date


class Sample(Base):
    """Sample.

    Retrieve a Sample based on accession code

        >>> import pyrefinebio
        >>> accession_code = "GSM000000"
        >>> sample = pyrefinebio.Sample.get(accession_code)

    Retrieve a list of Samples based on filters

        >>> import pyrefinebio
        >>> samples = pyrefinebio.Sample.search(is_processed=True, specimen_part="soft-tissue sarcoma")
    """

    def __init__(
        self=None,
        id=None,
        title=None,
        accession_code=None,
        source_database=None,
        organism=None,
        platform_accession_code=None,
        platform_name=None,
        pretty_platform=None,
        technology=None,
        manufacturer=None,
        protocol_info=None,
        annotations=None,
        results=None,
        source_archive_url=None,
        has_raw=None,
        sex=None,
        age=None,
        specimen_part=None,
        genotype=None,
        disease=None,
        disease_stage=None,
        cell_line=None,
        treatment=None,
        race=None,
        subject=None,
        compound=None,
        time=None,
        is_processed=None,
        is_unable_to_be_processed=None,
        created_at=None,
        last_modified=None,
        contributed_metadata=None,
        contributed_keywords=None,
        original_files=[],
        computed_files=[],
        last_processor_job=None,
        last_downloader_job=None,
        most_recent_smashable_file=None,
        most_recent_quant_file=None,
        experiment_accession_codes=None,
        experiments=None,
    ):
        super().__init__(identifier=accession_code)

        self.id = id
        self.title = title
        self.accession_code = accession_code
        self.source_database = source_database
        self.organism = prb_organism.Organism(**(organism)) if organism else None
        self.platform_accession_code = platform_accession_code
        self.platform_name = platform_name
        self.pretty_platform = pretty_platform
        self.technology = technology
        self.manufacturer = manufacturer
        self.protocol_info = protocol_info
        self.annotations = (
            [prb_annotation.Annotation(**annotation) for annotation in annotations]
            if annotations
            else []
        )
        self.results = (
            [prb_computational_result.ComputationalResult(**result) for result in results]
            if results
            else []
        )
        self.source_archive_url = source_archive_url
        self.has_raw = has_raw
        self.sex = sex
        self.age = age
        self.specimen_part = specimen_part
        self.genotype = genotype
        self.disease = disease
        self.disease_stage = disease_stage
        self.cell_line = cell_line
        self.treatment = treatment
        self.race = race
        self.subject = subject
        self.compound = compound
        self.time = time
        self.is_processed = is_processed
        self.is_unable_to_be_processed = is_unable_to_be_processed
        self.created_at = parse_date(created_at)
        self.last_modified = parse_date(last_modified)
        self.contributed_metadata = contributed_metadata

        self.original_files = (
            [prb_original_file.OriginalFile(id=file_id) for file_id in original_files]
            if original_files
            else []
        )
        self.computed_files = (
            [prb_computed_file.ComputedFile(id=file_id) for file_id in computed_files]
            if computed_files
            else []
        )

        # this isn't populated yet but the api does include these keys in the response
        # so for now let's just try to apply them
        if last_processor_job:
            self.last_processor_job = prb_job.ProcessorJob(**last_processor_job)
        if last_downloader_job:
            self.last_downloader_job = prb_job.DownloaderJob(**last_downloader_job)

        self.most_recent_smashable_file = most_recent_smashable_file
        self.most_recent_quant_file = most_recent_quant_file
        self.experiment_accession_codes = experiment_accession_codes
        self.experiments = experiments

        # Avoid initializing every Sample with the sample empty list as a default
        if not contributed_keywords:
            contributed_keywords = []

    @property
    def experiments(self):
        if not self._experiments:
            self._experiments = prb_experiment.Experiment.search(
                accession_code=self.experiment_accession_codes
            )

        return self._experiments

    @experiments.setter
    def experiments(self, value):
        self._experiments = value

    @classmethod
    def get(cls, accession_code):
        """Retrieve a Sample based on its accession code.

        Returns:
            Sample

        Parameters:
            accession_code (str): The accession code for the Sample to be retrieved.
        """
        response = get_by_endpoint("samples/" + accession_code).json()
        return cls(**response)

    @classmethod
    def search(cls, **kwargs):
        """Retrieve a list of Samples based on various filters

        Returns:
            list of Sample

        Keyword Arguments:
            ordering (str): which field to use when ordering the results

            title (str): filter based on the Sample's title

            organism__name (str): filter based on the Organism that the Sample was taken from

            organism__taxonomy_id (int): filter based on the Organism that the Sample was taken from

            source_database (str): filter based on the publically available repository
                                   that the Sample was taken from

            source_archive_url (str): filter based on Sample's source url

            has_raw (bool): filter based on if the Sample had raw data available in the source database

            platform_name (str): filter based on the name of the Platform that was used to assay the Sample

            technology (str): filter based on the technology that was used to assay the Sample

            manufacturer (str): filter based on the manufacturer of the technology that was used to assay the Sample

            sex (str): filter based on the sex information provided by the submitter

            age (number): filter based on the age information provided by the submitter

            specimen_part (str): filter based on the part of the specimen reported by the submitter

            genotype (str): filter based on the genotype of the subject that the Sample was taken from

            disease (str): filter based on the disease information provided by the submitter

            disease_stage (str): filter based on the disease stage information provided by the submitter

            cell_line (str): filter based on the cell line used for the sample

            treatment (str): filter based on the treatment information provided by the submitter

            race (str): filter based on the race information provided by the submitter

            subject (str): filter based on the subject identifier information provided by the submitter

            compound (str): filter based on the compound information provided by the submitter

            time (str): filter based on the time information provided by the submitter

            is_processed (bool): filter based on if the Sample has been processed

            limit (int): number of results to return per page.

            offset (int): the initial index from which to return the results.

            dataset_id (str): filter based on the Dataset ids that the Sample has been added to

            experiment_accession_code (str): filter based on the Experiments that are associated
                                             with the Sample

            accession_codes (str): filter based on multiple accession codes at once
        """
        response = get_by_endpoint("samples", params=kwargs)
        return create_paginated_list(cls, response)
