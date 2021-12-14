from pyrefinebio import job as prb_job, sample as prb_sample
from pyrefinebio.api_interface import get_by_endpoint
from pyrefinebio.base import Base
from pyrefinebio.util import create_paginated_list, parse_date


class OriginalFile(Base):
    """Original File.

    Retrieve an OriginalFile by id

        >>> import pyrefinebio
        >>> id = 1
        >>> og_file = pyrefinebio.OriginalFile.get(id)

    Retrieve a list of OriginalFiles based on filters

        >>> import pyrefinebio
        >>> og_files = pyrefinebio.OriginalFile.search()
    """

    def __init__(
        self,
        id=None,
        filename=None,
        size_in_bytes=None,
        sha1=None,
        samples=None,
        processor_jobs=None,
        downloader_jobs=None,
        source_url=None,
        source_filename=None,
        is_downloaded=None,
        is_archive=None,
        has_raw=None,
        created_at=None,
        last_modified=None,
    ):
        super().__init__(identifier=id)

        self.id = id
        self.filename = filename
        self.size_in_bytes = size_in_bytes
        self.sha1 = sha1
        samples_list = []
        if samples:
            for sample in samples:
                if type(sample) is dict:
                    samples_list.append(prb_sample.Sample(**sample))
                else:
                    samples_list.append(sample)

        self.samples = samples_list

        processor_jobs_list = []
        if processor_jobs:
            for processor_job in processor_jobs:
                if type(processor_job) is dict:
                    processor_jobs_list.append(prb_job.ProcessorJob(**processor_job))
                else:
                    processor_jobs_list.append(processor_job)

        self.processor_jobs = processor_jobs_list

        downloader_jobs_list = []
        if downloader_jobs:
            for downloader_job in downloader_jobs:
                if type(downloader_job) is dict:
                    downloader_jobs_list.append(prb_job.DownloaderJob(**downloader_job))
                else:
                    downloader_jobs_list.append(downloader_job)

        self.downloader_jobs = downloader_jobs_list

        self.source_url = source_url
        self.source_filename = source_filename
        self.is_downloaded = is_downloaded
        self.is_archive = is_archive
        self.has_raw = has_raw
        self.created_at = parse_date(created_at)
        self.last_modified = parse_date(last_modified)

    @classmethod
    def get(cls, id):
        """Retrieve an OriginalFile based on id

        Returns:
            OriginalFile

        Parameters:
            id (int): the id for the OriginalFile you want to get
        """

        response = get_by_endpoint("original_files/" + str(id)).json()
        return OriginalFile(**response)

    @classmethod
    def search(cls, **kwargs):
        """Retrieve a list of OriginalFiles based on various filters

        Returns:
            list of OriginalFile

        Keyword Arguments:

            id (int): filter based on the id of the OriginalFile

            filename (str): filter based on the name of the OriginalFile

            samples (str): filter based on the Samples associated with the OriginalFile

            size_in_bytes (int): filter based on the OriginalFile's size

            sha1 (str): filter based on the OriginalFiles sha1 hash

            processor_jobs (str): filter based on the ProcessorJobs associated with the OriginalFile

            downloader_jobs (str): filter based on the DownloaderJobs associated with the OriginalFile

            source_url (str): filter based on the OriginalFile's source url

            is_archive (bool): filter based on if the OriginalFile is archived

            source_filename (str): filter based on the OriginalFile's source's filename

            has_raw (bool): filter based on if the OriginalFile had raw data available in the source
                            database

            created_at (str): filter based on the time when the OriginalFile was created

            last_modified (str): filter based on the time when the OriginalFile was last modified

            ordering (str): which field to use when ordering the results.

            limit (int): number of results to return per page.

            offset (int): the initial index from which to return the results.
        """

        response = get_by_endpoint("original_files", params=kwargs)
        return create_paginated_list(cls, response)
