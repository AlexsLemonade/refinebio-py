from pyrefinebio import original_file as prb_original_file
from pyrefinebio.api_interface import get_by_endpoint
from pyrefinebio.base import Base
from pyrefinebio.util import create_paginated_list, parse_date


class DownloaderJob(Base):
    """DownloaderJob.

    Retrieve a DownloaderJob by id

        >>> import pyrefinebio
        >>> id = 1
        >>> job = pyrefinebio.DownloaderJob.get(id)

    Retrieve a list of DownloaderJobs based on filters

        >>> import pyrefinebio
        >>> jobs = pyrefinebio.DownloaderJob.search(batch_job_id=0, success=True)
    """

    def __init__(
        self,
        id=None,
        downloader_task=None,
        num_retries=None,
        retried=None,
        was_recreated=None,
        worker_id=None,
        ram_amount=None,
        worker_version=None,
        batch_job_id=None,
        batch_job_queue=None,
        failure_reason=None,
        success=None,
        original_files=[],
        start_time=None,
        end_time=None,
        created_at=None,
        last_modified=None,
        is_queued=None,
    ):
        super().__init__(identifier=id)

        self.id = id
        self.downloader_task = downloader_task
        self.num_retries = num_retries
        self.retried = retried
        self.was_recreated = was_recreated
        self.worker_id = worker_id
        self.ram_amount = ram_amount
        self.worker_version = worker_version
        self.batch_job_id = batch_job_id
        self.batch_job_queue = batch_job_queue
        self.failure_reason = failure_reason
        self.success = success
        self.start_time = parse_date(start_time)
        self.end_time = parse_date(end_time)
        self.created_at = parse_date(created_at)
        self.last_modified = parse_date(last_modified)
        self.is_queued = is_queued

        original_files_list = []
        if original_files:
            for original_file in original_files:
                if type(original_file) is dict:
                    original_files_list.append(prb_original_file.OriginalFile(**original_file))
                elif type(original_file) is int:
                    original_files_list.append(prb_original_file.OriginalFile(id=original_file))
                else:
                    original_files_list.append(original_file)

        self.original_files = original_files_list

    @classmethod
    def get(cls, id):
        """Retrieve a DownloaderJob based on id

        Returns:
            DownloaderJob

        Parameters:
            id (int): the id for the DownloaderJob you want to get
        """
        response = get_by_endpoint("jobs/downloader/" + str(id)).json()
        return DownloaderJob(**response)

    @classmethod
    def search(cls, **kwargs):
        """Retrieve a list of DownloaderJobs based on various filters

        Returns:
            list of DownloaderJob

        Keyword Arguments:

            id (int): filter based on the id of the DownloaderJob

            downloader_task (str): filter based on the job's task type

            num_retries (int): filter based on the number of times the job has retried

            retried (bool): filter based on if the job has retried

            was_recreated (bool): filter based on if the job was recreated

            worker_id (str): filter based on the job's worker id

            ram_amount (int): filter based on the amount of ram assigned to the job

            worker_version (str): filter based on the job's worker version

            batch_job_id (str): filter based on the job's batch id

            failure_reason (str): filter based on the reason why the job failed

            success (bool): filter based on if the job succeeded

            original_files (str): filter based on the ids of the OriginalFiles associated with the job

            start_time (str): filter based on the time when the job started

            end_time (str): filter based on the time when the job finished

            created_at (str): filter based on the time that the job was created

            last_modified (str): filter based on the time that the job was last modified

            ordering (str): which field to use when ordering the results.

            limit (int): number of results to return per page.

            offset (int): the initial index from which to return the results.

            sample_accession_code (str): filter based on the Samples associated with the job
        """
        response = get_by_endpoint("jobs/downloader", params=kwargs)
        return create_paginated_list(cls, response)


class ProcessorJob(Base):
    """Processor Job.

    Retrieve a ProcessorJob by id

        >>> import pyrefinebio
        >>> id = 1
        >>> job = pyrefinebio.ProcessorJob.get(id)

    Retrieve a list of ProcessorJobs based on filters

        >>> import pyrefinebio
        >>> jobs = pyrefinebio.ProcessorJob.search(num_retries=1)
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
        batch_job_id=None,
        batch_job_queue=None,
        success=None,
        original_files=[],
        datasets=None,
        start_time=None,
        end_time=None,
        created_at=None,
        last_modified=None,
        is_queued=None,
    ):
        super().__init__(identifier=id)

        self.id = id
        self.pipeline_applied = pipeline_applied
        self.num_retries = num_retries
        self.retried = retried
        self.worker_id = worker_id
        self.ram_amount = ram_amount
        self.volume_index = volume_index
        self.worker_version = worker_version
        self.failure_reason = failure_reason
        self.batch_job_id = batch_job_id
        self.batch_job_queue = batch_job_queue
        self.success = success
        self.datasets = datasets
        self.start_time = parse_date(start_time)
        self.end_time = parse_date(end_time)
        self.created_at = parse_date(created_at)
        self.last_modified = parse_date(last_modified)
        self.is_queued = is_queued

        original_files_list = []
        if original_files:
            for original_file in original_files:
                if type(original_file) is dict:
                    original_files_list.append(prb_original_file.OriginalFile(**original_file))
                elif type(original_file) is int:
                    original_files_list.append(prb_original_file.OriginalFile(id=original_file))
                else:
                    original_files_list.append(original_file)

        self.original_files = original_files_list

    @classmethod
    def get(cls, id):
        """Retrieve a ProcessorJob based on id

        Returns:
            ProcessorJob

        Parameters:
            id (int): the id for the ProcessorJob you want to get
        """
        response = get_by_endpoint("jobs/processor/" + str(id)).json()
        return ProcessorJob(**response)

    @classmethod
    def search(cls, **kwargs):
        """Retrieve a list of ProcessorJobs based on various filters

        Returns:
            list of ProcessorJob

        Keyword Arguments:
            id (int): filter based on the id of the ProcessorJob

            pipeline_applied (str): filter based on the type of pipeline applied to the job

            num_retries (int): filter based on the number of times the job has retried

            retried (bool): filter based on if the job has retried

            worker_id (str): filter based on the id of the job's worker

            ram_amount (int): filter based on the amount of ram assigned to the job

            volume_index (str):

            worker_version (str): filter based on the job's worker version

            failure_reason (str): filter based on the reason why the job failed

            batch_job_id (str): filter based on the job's batch id

            success (bool): filter based on if the job has succeeded

            original_files (str): filter based on the ids of the OriginalFiles associated with the job

            datasets (str): filter based on the ids of the Datasets associated with the job

            start_time (str): filter based on the time when the job started

            end_time (str): filter based on the time when the job finished

            created_at (str): filter based on the time when the job was created

            last_modified (str): filter based on the time when the job was last modified

            ordering (str): which field to use when ordering the results.

            limit (int): number of results to return per page.

            offset (int): the initial index from which to return the results.

            sample_accession_code (str): filter based on the samples associated with the job
        """
        response = get_by_endpoint("jobs/processor", params=kwargs)
        return create_paginated_list(cls, response)


class SurveyJob(Base):
    """Survey Job.

    Retrieve a SurveyJob by id

        >>> import pyrefinebio
        >>> id = 1
        >>> job = pyrefinebio.SurveyJob.get(id)

    Retrieve a list of SurveyJobs based on filters

        >>> import pyrefinebio
        >>> jobs = pyrefinebio.SurveyJob.search(num_retries=1)
    """

    def __init__(
        self,
        id=None,
        source_type=None,
        success=None,
        ram_amount=None,
        start_time=None,
        end_time=None,
        batch_job_id=None,
        batch_job_queue=None,
        created_at=None,
        last_modified=None,
        is_queued=None,
    ):
        super().__init__(identifier=id)

        self.id = id
        self.source_type = source_type
        self.success = success
        self.ram_amount = ram_amount
        self.start_time = parse_date(start_time)
        self.end_time = parse_date(end_time)
        self.batch_job_id = batch_job_id
        self.batch_job_queue = batch_job_queue
        self.created_at = parse_date(created_at)
        self.last_modified = parse_date(last_modified)
        self.is_queued = is_queued

    @classmethod
    def get(cls, id):
        """Retrieve a SurveyJob based on id

        Returns:
            SurveyJob

        Parameters:
            id (int): the id for the SurveyJob you want to get
        """
        response = get_by_endpoint("jobs/survey/" + str(id)).json()
        return SurveyJob(**response)

    @classmethod
    def search(cls, **kwargs):
        """Retrieve a list of SurveyJobs based on various filters

        Returns:
            list of SurveyJob

        Keyword Arguments:
            id (int): filter based on the id of the SurveyJob

            source_type (str): filter based on the name of the source database

            success (bool): filter based on if the job has succeeded

            ram_amount (int): filter based on the amount of ram assigned to the job

            start_time (str): filter based on the time when the job started

            end_time (str): filter based on the time when the job finished

            created_at (str): filter based on the time when the job was created

            last_modified (str): filter based on the time when the job was last modified

            ordering (str): which field to use when ordering the results.

            limit (int): number of results to return per page.

            offset (int): the initial index from which to return the results.
        """
        response = get_by_endpoint("jobs/survey", params=kwargs)
        return create_paginated_list(cls, response)
