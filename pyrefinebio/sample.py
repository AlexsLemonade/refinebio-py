from pyrefinebio.http import get_by_endpoint
from pyrefinebio.util import generator_from_pagination, parse_date

from pyrefinebio.common import annotation as prb_annotation
from pyrefinebio import computational_result as prb_computational_result
from pyrefinebio import experiment as prb_experiment
from pyrefinebio import organism as prb_organism


class Sample:
    """Sample.

    Retrieve a sample based on accession code

        ex:
        >>> import pyrefinebio
        >>> accession_code = "GSM000000"
        >>> sample = pyrefinebio.Sample.get(accession_code)

    Retrieve a list of samples based on filters

        ex:
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
        created_at=None,
        last_modified=None,
        original_files=None,
        computed_files=None,
        experiment_accession_codes=None,
        experiments=None,
    ):
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
        self.created_at = parse_date(created_at)
        self.last_modified = parse_date(last_modified)
        self.original_files = original_files
        self.computed_files = computed_files
        self.experiment_accession_codes = experiment_accession_codes
        self.experiments = experiments

    @property
    def experiments(self):
        if not self._experiments:
            self._experiments = prb_experiment.Experiment.search(
                accession_codes=self.experiment_accession_codes
            )

        return self._experiments

    @experiments.setter
    def experiments(self, value):
        self._experiments = value

    @classmethod
    def get(cls, accession_code):
        """Retrieve a sample based on its accession code.

        returns: Sample

        parameters:

            accession_code (str): The accession code for the sample to be retrieved.
        """
        result = get_by_endpoint("samples/" + accession_code)
        return cls(**result)

    @classmethod
    def search(cls, **kwargs):
        """Retrieve a list of samples based on various filters

        returns: list of samples.

        Parameters:
            ordering (str): which field to use when ordering the results

            title (str): filter based on the sample's title

            organism (str): filter based on the organism that the sample was taken from

            source_database (str): filter based on the database that the sample was taken from

            source_archive_url (str): filter based on sample's source url

            has_raw (bool): filter based on if the sample

            platform_name (str): filter based on the name of the platform that was used to create the sample

            technology (str): filter based on the technology that was used to make the sample

            manufacturer (str): filter based on the manufacturer of the technology that was used to create the sample

            sex (str): filter based on the sex of the organism that the sample was taken from

            age (number): filter based on the age of the organism that the sample was taken from

            specimen_part (str): filter based on the part of the specimen that the sample was taken from

            genotype (str): filter based on the genotype 

            disease (str): filter based on the disease

            disease_stage (str): filter based on the stage of the disease

            cell_line (str):

            treatment (str): filter based on the treatment used for the sample subject's disease

            race (str): filter based on the race of the sample's subject 

            subject (str): filter based on the name of the sample's subject

            compound (str):

            time (str): filter based on the time

            is_processed (bool): filter based on if the sample has been processed

            is_public (bool): filter based on if the sample is public

            limit (int): number of results to return per page.

            offset (int): the initial index from which to return the results.

            dataset_id (str): filter based on the dataset id that the sample has been added to

            experiment_accession_code (str): filter based on the experiments that are associated
                                             with the sample

            accession_codes (str): filter based on multiple accession codes at once
        """
        result = get_by_endpoint("samples", params=kwargs)
        return generator_from_pagination(result, cls)
