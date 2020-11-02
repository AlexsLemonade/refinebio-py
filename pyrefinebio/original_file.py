from pyrefinebio.http import get_by_endpoint
from pyrefinebio.util import generator_from_pagination, parse_date

import pyrefinebio.job as prb_job
import pyrefinebio.sample as prb_sample


class OriginalFile:
    """Original File.

    Retrieve an original file by id

        ex:
        >>> import pyrefinebio
        >>> id = 1
        >>> og_file = pyrefinebio.OriginalFile.get(id)

    Retrieve a list of original files based on filters

        ex:
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
        self.id = id
        self.filename = filename
        self.size_in_bytes = size_in_bytes
        self.sha1 = sha1
        self.samples = [prb_sample.Sample(**sample) if type(sample) is dict else sample for sample in samples] if samples else []
        self.processor_jobs = [prb_job.ProcessorJob(**processor_job) if type(processor_job) is dict else processor_job for processor_job in processor_jobs] if processor_jobs else []
        self.downloader_jobs = [prb_job.DownloaderJob(**downloader_job) if type(downloader_job) is dict else downloader_job for downloader_job in downloader_jobs] if downloader_jobs else []
        self.source_url = source_url
        self.source_filename = source_filename
        self.is_downloaded = is_downloaded
        self.is_archive = is_archive
        self.has_raw = has_raw
        self.created_at = parse_date(created_at)
        self.last_modified = parse_date(last_modified)

    @classmethod
    def get(cls, id):
        """Retrieve an original file based on id

        returns: OriginalFile

        parameters:

            id (int): the id for the original file you want to get
        """

        response = get_by_endpoint("original_files/" + str(id))
        return OriginalFile(**response)

    @classmethod
    def search(cls, **kwargs):
        """Retrieve a list of original files based on various filters

        returns: list of OriginalFile

        valid filters:

            id (int): filter based on the id of the original file
            
            filename (str): filter based on the name of the original file
            
            samples (str): filter based on the samples associated with the original file
            
            size_in_bytes (int): filter based on the original file's size 
            
            sha1 (str): filter based on the original files sha1 hash
            
            processor_jobs (str): filter based on the processor jobs associated with the original file
            
            downloader_jobs (str): filter based on the downloader jobs associated with the original file
            
            source_url (str): filter based on the original file's source url
            
            is_archive (bool): filter based on if the original file is archived
            
            source_filename (str): filter based on the original file's source's filename
            
            has_raw (bool):
            
            created_at (str): filter based on the time when the original file was created
            
            last_modified (str): filter based on the time when the original file was last modified
            
            ordering (str): which field to use when ordering the results.

            limit (int): number of results to return per page.

            offset (int): the initial index from which to return the results.
        """

        response = get_by_endpoint("original_files", params=kwargs)
        return generator_from_pagination(response, cls)
