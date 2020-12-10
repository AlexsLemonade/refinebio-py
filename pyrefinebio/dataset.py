from pyrefinebio.http import get_by_endpoint, post_by_endpoint, put_by_endpoint, download_file
from pyrefinebio.exceptions import DownloadError
from pyrefinebio.util import parse_date

import pyrefinebio.experiment as prb_experiment
import pyrefinebio.sample as prb_sample


class Dataset:
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
        download_url=None
    ):
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
        experiment = experiment.accession_code if isinstance(experiment, prb_experiment.Experiment) else experiment
        samples = [sample.accession_code if isinstance(sample, prb_sample.Sample) else sample for sample in samples]

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
        if self.aggregate_by:
            body["aggregate_by"] = self.aggregate_by
        if self.scale_by:
            body["scale_by"] = self.scale_by
        if self.email_address:
            body["email_address"] = self.email_address
        if self.email_ccdl_ok:
            body["email_ccdl_ok"] = self.email_ccdl_ok
        if self.start:
            body["start"] = self.start
        if self.quantile_normalize:
            body["quantile_normalize"] = self.quantile_normalize
        if self.quant_sf_only:
            body["quant_sf_only"] = self.quant_sf_only
        if self.svd_algorithm:
            body["svd_algorithm"] = self.svd_algorithm

        if self.id:
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


    def download(self, path):
        """Download a processed Dataset

        Returns:
            void

        Parameters:
            path (str): the path that the Dataset should be downloaded to
        """
        download_url = self.download_url or self.get(self.id).download_url

        if not download_url:
            raise DownloadError("dataset", "Download url not found - did you process the dataset?")

        download_file(download_url, path)
