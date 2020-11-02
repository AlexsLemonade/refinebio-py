from pyrefinebio.http import get_by_endpoint
from pyrefinebio.util import generator_from_pagination, parse_date


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
        was_recreated=None,
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
        self.was_recreated = was_recreated
        self.worker_id = worker_id
        self.worker_version = worker_version
        self.nomad_job_id = nomad_job_id
        self.failure_reason = failure_reason
        self.success = success
        self.original_files = original_files
        self.start_time = parse_date(start_time)
        self.end_time = parse_date(end_time)
        self.created_at = parse_date(created_at)
        self.last_modified = parse_date(last_modified)

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

        valid filters:

            id (int): filter based on the id of the downloader job

            downloader_task (str): filter based on the  task 
            
            num_retries (int): filter based on the number of times the job has retried

            retried (bool): filter based on if the job has retried
            
            was_recreated (bool): filter based on if the job was recreated
            
            worker_id (str): filter based on the job's worker id
            
            worker_version (str): filter based on the job's worker version
            
            nomad_job_id (str): filter based on the job's nomad id
            
            failure_reason (str): filter based on the reason why the job failed
            
            success (bool): filter based on if the job succeeded
            
            original_files (str): filter based on the ids of the original files associated with the job
            
            start_time (str): filter based on the time when the job started
            
            end_time (str): filter based on the time when the job finished
            
            created_at (str): filter based on the time that the job was created
            
            last_modified (str): filter based on the time that the job was last modified
            
            ordering (str): which field to use when ordering the results.

            limit (int): number of results to return per page.

            offset (int): the initial index from which to return the results.

            sample_accession_code (str): filter based on the samples associated with the job

            nomad (bool): filter based on if the job is in the nomad queue currently
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
        self.start_time = parse_date(start_time)
        self.end_time = parse_date(end_time)
        self.created_at = parse_date(created_at)
        self.last_modified = parse_date(last_modified)

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

            id (int): filter based on the id of the downloader job
            
            pipeline_applied (str):
            
            num_retries (int): filter based on the number of times the job has retried
            
            retried (bool): filter based on if the job has retried
            
            worker_id (str): filter based on the id of the job's worker
            
            ram_amount (int): filter based on the amount of ram assigned to the job
            
            volume_index (str):
            
            worker_version (str): filter based on the job's worker version
            
            failure_reason (str): filter based on the reason why the job failed
            
            nomad_job_id (str): filter based on the job's nomad id
            
            success (bool): filter based on if the job has succeeded
            
            original_files (str): filter based on the ids of the original files associated with the job
            
            datasets (str): filter based on the ids of the datasets associated with the job
            
            start_time (str): filter based on the time when the job started
            
            end_time (str): filter based on the time when the job finished
            
            created_at (str): filter based on the time when the job was created
            
            last_modified (str): filter based on the time when the job was last modified
            
            ordering (str): which field to use when ordering the results.

            limit (int): number of results to return per page.

            offset (int): the initial index from which to return the results.

            sample_accession_code (str): filter based on the samples associated with the job

            nomad (bool): filter based on if the job is in the nomad queue currently
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
        self.start_time = parse_date(start_time)
        self.end_time = parse_date(end_time)
        self.created_at = parse_date(created_at)
        self.last_modified = parse_date(last_modified)

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

        valid filters:

            id (int): filter based on the id of the survey job
                
            source_type (str): 
            
            success (bool): filter based on if the job has succeeded
            
            start_time (str): filter based on the time when the job started
            
            end_time (str): filter based on the time when the job finished
            
            created_at (str): filter based on the time when the job was created
            
            last_modified (str): filter based on the time when the job was last modified
            
            ordering (str): which field to use when ordering the results.

            limit (int): number of results to return per page.

            offset (int): the initial index from which to return the results.
        """
        response = get_by_endpoint("jobs/survey", params=kwargs)
        return generator_from_pagination(response, cls)
