from pyrefinebio.http import get_by_endpoint
from pyrefinebio.util import generator_from_pagination


class DownloaderJob:
    """DownloaderJob.

    Retrieve a downloader job by id

        ex:
        >>> import pyrefinebio
        >>> id = 1
        >>> job = pyrefinebio.DownloaderJob.get(id)

    Retrieve a list of downloader jobs based on filters

        ex:
        >>> import pyrefinebio
        >>> jobs = pyrefinebio.DownloaderJob.search(nomad_job_id=0, success=True)
    """

    def __init__(
        self,
        id=None,
        downloader_task=None,
        num_retries=None,
        retried=None,
        was_recorded=None,
        worker_id=None,
        worker_version=None,
        nomad_job_id=None,
        failure_reason=None,
        success=None,
        original_files=None,
        start_time=None,
        end_time=None,
        created_at=None,
        last_modified=None,
    ):
        self.id = id
        self.downloader_task = downloader_task
        self.num_retries = num_retries
        self.retried = retried
        self.was_recorded = was_recorded
        self.worker_id = worker_id
        self.worker_version = worker_version
        self.nomad_job_id = nomad_job_id
        self.failure_reason = failure_reason
        self.success = success
        self.original_files = original_files
        self.start_time = start_time
        self.end_time = end_time
        self.created_at = created_at
        self.last_modified = last_modified

    @classmethod
    def get(cls, id):
        """Retrieve a downloader job based on id

        returns: DownloaderJob

        parameters:

            id (int): the id for the downloader job you want to get
        """
        response = get_by_endpoint("jobs/downloader/" + str(id))
        return DownloaderJob(**response)

    @classmethod
    def search(cls, **kwargs):
        """Retrieve a list of downloader jobs based on various filters

        returns: list of DownloaderJob

        parameters:

            id (int):

            downloader_task (str):
            
            num_retries (int):

            retried (str):
            
            was_recreated (str):
            
            worker_id (str):
            
            worker_version (str):
            
            nomad_job_id (str):
            
            failure_reason (str):
            
            success (str):
            
            original_files (str):
            
            start_time (str):
            
            end_time (str):
            
            created_at (str):
            
            last_modified (str):
            
            ordering (str): Which field to use when ordering the results.

            limit (int): Number of results to return per page.

            offset (int): The initial index from which to return the results.

            sample_accession_code (str): List the downloader jobs associated with a sample

            nomad (str): Only return jobs that are in the nomad queue currently
        """
        response = get_by_endpoint("jobs/downloader", params=kwargs)
        return generator_from_pagination(response, cls)


class ProcessorJob:
    """Processor Job.

    Retrieve a processor job by id

        ex:
        >>> import pyrefinebio
        >>> id = 1
        >>> job = pyrefinebio.DownloaderJob.get(id)

    Retrieve a list of processor jobs based on filters

        ex:
        >>> import pyrefinebio
        >>> jobs = pyrefinebio.DownloaderJob.search(num_retries=1)
    """

    def __init__(
        self,
        id=None,
        pipeline_applied=None,
        num_retries=None,
        retried=None,
        worker_id=None,
        ram_amount=None,
        volume_index=None,
        worker_version=None,
        failure_reason=None,
        nomad_job_id=None,
        success=None,
        original_files=None,
        datasets=None,
        start_time=None,
        end_time=None,
        created_at=None,
        last_modified=None,
    ):
        self.id = id
        self.pipeline_applied = pipeline_applied
        self.num_retries = num_retries
        self.retried = retried
        self.worker_id = worker_id
        self.ram_amount = ram_amount
        self.volume_index = volume_index
        self.worker_version = worker_version
        self.failure_reason = failure_reason
        self.nomad_job_id = nomad_job_id
        self.success = success
        self.original_files = original_files
        self.datasets = datasets
        self.start_time = start_time
        self.end_time = end_time
        self.created_at = created_at
        self.last_modified = last_modified

    @classmethod
    def get(cls, id):
        """Retrieve a processor job based on id

        returns: ProcessorJob

        parameters:

            id (int): the id for the processor job you want to get
        """
        response = get_by_endpoint("jobs/processor/" + str(id))
        return ProcessorJob(**response)

    @classmethod
    def search(cls, **kwargs):
        """Retrieve a list of processor jobs based on various filters

        returns: list of ProcessorJob

        parameters:

            id (number):
            
            pipeline_applied (string):
            
            num_retries (number):
            
            retried (string):
            
            worker_id (string):
            
            ram_amount (number):
            
            volume_index (string):
            
            worker_version (string):
            
            failure_reason (string):
            
            nomad_job_id (string):
            
            success (string):
            
            original_files (string):
            
            datasets (string):
            
            start_time (string):
            
            end_time (string):
            
            created_at (string):
            
            last_modified (string):
            
            ordering (string): Which field to use when ordering the results.

            limit (integer): Number of results to return per page.

            offset (integer): The initial index from which to return the results.

            sample_accession_code (string): List the processor jobs associated with a sample

            nomad (string): Only return jobs that are in the nomad queue currently
        """
        response = get_by_endpoint("jobs/processor", params=kwargs)
        return generator_from_pagination(response, cls)


class SurveyJob:
    """Survey Job.

    Retrieve a survey job by id

        ex:
        >>> import pyrefinebio
        >>> id = 1
        >>> job = pyrefinebio.SurveyJob.get(id)

    Retrieve a list of survey jobs based on filters

        ex:
        >>> import pyrefinebio
        >>> jobs = pyrefinebio.SurveyJob.search(num_retries=1)
    """

    def __init__(
        self,
        id=None,
        source_type=None,
        success=None,
        start_time=None,
        end_time=None,
        created_at=None,
        last_modified=None,
    ):
        self.id = id
        self.source_type = source_type
        self.success = success
        self.start_time = start_time
        self.end_time = end_time
        self.created_at = created_at
        self.last_modified = last_modified

    @classmethod
    def get(cls, id):
        """Retrieve a survey job based on id

        returns: SurveyJob

        parameters:

            id (int): the id for the survey job you want to get
        """
        response = get_by_endpoint("jobs/survey/" + str(id))
        return SurveyJob(**response)

    @classmethod
    def search(cls, **kwargs):
        """Retrieve a list of survey jobs based on various filters

        returns: list of SurveyJob

        parameters:

            id (number):
                
            source_type (string):
            
            success (string):
            
            start_time (string):
            
            end_time (string):
            
            created_at (string):
            
            last_modified (string):
            
            ordering (string): Which field to use when ordering the results.

            limit (integer): Number of results to return per page.

            offset (integer): The initial index from which to return the results.
        """
        response = get_by_endpoint("jobs/survey", params=kwargs)
        return generator_from_pagination(response, cls)
