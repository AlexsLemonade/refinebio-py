import pyrefinebio.job as prb_job
import pyrefinebio.sample as prb_sample
from pyrefinebio.http import get_by_endpoint
from pyrefinebio.util import generator_from_pagination


class OriginalFile:
    """Original File.

    get an original file by id

        ex:
        >>> import pyrefinebio
        >>> id = 1
        >>> job = pyrefinebio.OriginalFile.get(id)

    search for an original file based on filters

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
        samples=[],
        processor_jobs=[],
        downloader_jobs=[],
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
        self.samples = [prb_sample.Sample(**sample) for sample in samples]
        self.processor_jobs = [
            prb_job.ProcessorJob(**processor_job) for processor_job in processor_jobs
        ]
        self.downloader_jobs = [
            prb_job.DownloaderJob(**downloader_job) for downloader_job in downloader_jobs
        ]
        self.source_url = source_url
        self.source_filename = source_filename
        self.is_downloaded = is_downloaded
        self.is_archive = is_archive
        self.has_raw = has_raw
        self.created_at = created_at
        self.last_modified = last_modified

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
        """Retrieve an list of original files based on various filters

        returns: list of OriginalFile

        parameters:

            id (int):
            
            filename (str):
            
            samples (str):
            
            size_in_bytes (int):
            
            sha1 (str):
            
            processor_jobs (str):
            
            downloader_jobs (str):
            
            source_url (str):
            
            is_archive (str):
            
            source_filename (str):
            
            has_raw (str):
            
            created_at (str):
            
            last_modified (str):
            
            ordering (str): Which field to use when ordering the results.

            limit (int): Number of results to return per page.

            offset (int): The initial index from which to return the results.
        """

        response = get_by_endpoint("original_files", params=kwargs)
        return generator_from_pagination(response, cls)
