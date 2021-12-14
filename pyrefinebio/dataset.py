import shutil

from pyrefinebio import experiment as prb_experiment, sample as prb_sample
from pyrefinebio.api_interface import (
    download_file,
    get_by_endpoint,
    post_by_endpoint,
    put_by_endpoint,
)
from pyrefinebio.base import Base
from pyrefinebio.exceptions import DownloadError, MissingFile
from pyrefinebio.util import expand_path, parse_date


class Dataset(Base):
    """Dataset

    Datasets are collections of experiments and their samples.
    A Dataset needs to be constructed and then processed before it can be downloaded.
    Downloading a Dataset requires an activated API token. See `pyrefinebio.Token` for more details

    Create and save a Dataset

        >>> import pyrefinebio
        >>> dataset = pyrefinebio.Dataset(email_address="example@refine.bio", data={"SRP003819": ["SRR069230"]})
        >>> dataset = dataset.save()

    Get a Dataset that has been saved

        >>> import pyrefinebio
        >>> id = "dataset id <guid>"
        >>> dataset = pyrefinebio.Dataset.get(id)

    Start processing a Dataset

        >>> import pyrefinebio
        >>> dataset = pyrefinebio.Dataset(...)
        >>> dataset.process()

    Check if a Dataset is finished processing

        >>> import pyrefinebio
        >>> dataset = pyrefinebio.Dataset(...)
        >>> dataset.process()
        >>> dataset.check()

    Download a processed Dataset

        >>> import pyrefinebio
        >>> dataset = pyrefinebio.Dataset(...)
        >>> dataset.process()
        >>> dataset.download("~/datasets/my_dataset.zip")
    """

    def __init__(
        self,
        id=None,
        data=None,
        aggregate_by=None,
        scale_by=None,
        is_processing=None,
        is_processed=None,
        is_available=None,
        has_email=None,
        email_address=None,
        email_ccdl_ok=None,
        expires_on=None,
        s3_bucket=None,
        s3_key=None,
        success=None,
        failure_reason=None,
        created_at=None,
        last_modified=None,
        start=None,
        size_in_bytes=None,
        sha1=None,
        quantile_normalize=None,
        quant_sf_only=None,
        svd_algorithm=None,
        download_url=None,
        # Emails should be opt-in https://github.com/AlexsLemonade/refinebio-py/issues/58
        notify_me=False,
    ):
        super().__init__(identifier=id)

        self.id = id
        self.data = data
        self.aggregate_by = aggregate_by
        self.scale_by = scale_by
        self.is_processing = is_processing
        self.is_processed = is_processed
        self.is_available = is_available
        self.has_email = has_email
        self.email_address = email_address
        self.email_ccdl_ok = email_ccdl_ok
        self.expires_on = parse_date(expires_on)
        self.s3_bucket = s3_bucket
        self.s3_key = s3_key
        self.success = success
        self.failure_reason = failure_reason
        self.created_at = parse_date(created_at)
        self.last_modified = parse_date(last_modified)
        self.start = start
        self.size_in_bytes = size_in_bytes
        self.sha1 = sha1
        self.quantile_normalize = quantile_normalize
        self.quant_sf_only = quant_sf_only
        self.svd_algorithm = svd_algorithm
        self.download_url = download_url
        self.notify_me = notify_me

        self._downloaded_path = None

    @classmethod
    def get(cls, id):
        """Retrieve a specific Dataset based on id

        Returns:
            Dataset

        Parameters:
            id (str): the guid id for the computed file you want to get
        """
        response = get_by_endpoint("dataset/" + id).json()
        return Dataset(**response)

    def add_samples(self, experiment, samples=["ALL"]):
        """Add samples to a dataset

        Returns:
            Dataset

        Parameters:
            experiment (str): accession code for the Experiment related to the Samples you
                              are adding to the dataset
                       (Experiment): Experiment object related to the Samples you are adding
                              the dataset

            samples (list): list of Sample objects or Sample accession codes for the samples
                            you are adding to the dataset
        """
        if self.is_processing or self.is_processed:
            print("Cannot add samples to a dataset that has been processed!")
            return

        # get accession codes if Experiment or Sample objects are passed in
        if isinstance(experiment, prb_experiment.Experiment):
            experiment = experiment.accession_code

        sample_accession_codes = []
        for sample in samples:
            if isinstance(sample, prb_sample.Sample):
                sample_accession_codes.append(sample.accession_code)
            else:
                sample_accession_codes.append(sample)

        samples = sample_accession_codes

        if self.data:
            self.data[experiment] = samples
        else:
            self.data = {experiment: samples}

        return self

    def save(self):
        """Save a Dataset

        In order for a dataset to be saved its `data` attribute must be properly set.
        The `data` attribute should be a dict with experiment accession codes as the keys
        and lists of sample accession codes as the values. If you want all samples associated
        with the experiment, you can use the value `"ALL"`.

        Example:
            >>> data = {
            >>>     "SRP003819": [
            >>>         "SRR069230",
            >>>         "SRR069231"
            >>>     ],
            >>>     "SRP003820": ["ALL"]
            >>> }

        Returns:
            Dataset
        """
        body = {}
        body["data"] = self.data
        if self.aggregate_by is not None:
            body["aggregate_by"] = self.aggregate_by
        if self.scale_by is not None:
            body["scale_by"] = self.scale_by
        if self.email_address is not None:
            body["email_address"] = self.email_address
        if self.email_ccdl_ok is not None:
            body["email_ccdl_ok"] = self.email_ccdl_ok
        if self.start is not None:
            body["start"] = self.start
        if self.quantile_normalize is not None:
            body["quantile_normalize"] = self.quantile_normalize
        if self.quant_sf_only is not None:
            body["quant_sf_only"] = self.quant_sf_only
        if self.svd_algorithm is not None:
            body["svd_algorithm"] = self.svd_algorithm
        if self.notify_me is not None:
            body["notify_me"] = self.notify_me

        if self.id is not None:
            response = put_by_endpoint("dataset/" + self.id, payload=body).json()
        else:
            response = post_by_endpoint("dataset", payload=body).json()

        # add fields that aren't returned by the api
        response["email_address"] = self.email_address
        response["email_ccdl_ok"] = self.email_ccdl_ok

        for key, value in response.items():
            setattr(self, key, value)

        return self

    def process(self):
        """Start processing a Dataset

        In order for a Dataset to be processed, its `data` and `email_address` attributes
        must be properly set.

        Returns:
            void
        """
        self.start = True
        response = self.save()
        self.is_processing = response.is_processing

    def check(self):
        """Check to see if a Dataset has finished processing

        Returns:
            bool
        """

        response = self.get(self.id)
        self.is_processing = response.is_processing
        self.is_processed = response.is_processed
        return response.is_processed

    def download(self, path, prompt=True):
        """Download a processed Dataset

        The path that the dataset is downloaded to is stored in `_downloaded_path`

        Returns:
            Dataset

        Parameters:
            path (str): the path that the Dataset should be downloaded to

            prompt (bool): if true, will prompt before downloading files bigger than 1GB
        """
        download_url = self.download_url or self.get(self.id).download_url

        if not download_url:
            if self.check():
                raise DownloadError(
                    "Dataset",
                    "Download url not found - make sure you have set up and activated your Token. "
                    "You can create and activate a new token using pyrefinebio.create_token(). "
                    "See documentation for advanced usage: https://alexslemonade.github.io/refinebio-py/token.html",
                )
            else:
                raise DownloadError(
                    "Dataset",
                    "Download url not found - you must process the Dataset before downloading.",
                )

        full_path = expand_path(path, "dataset-" + str(self.id) + ".zip")

        download_file(download_url, full_path, prompt)

        self._downloaded_path = full_path

        return self

    def extract(self):
        """Extract a downloaded Dataset

        Returns:
            Dataset
        """
        if not self._downloaded_path:
            raise MissingFile(
                "Dataset downloaded file"
                "Make sure you have successfully downloaded the Dataset before extracting."
            )

        shutil.unpack_archive(self._downloaded_path)
        return self
