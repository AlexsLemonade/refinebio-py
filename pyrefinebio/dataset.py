from pyrefinebio.http import get_by_endpoint, post_by_endpoint, put_by_endpoint, download_file
from pyrefinebio.exceptions import DownloadError

from pyrefinebio.util import parse_date


class Dataset:

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
        response = get_by_endpoint("dataset/" + id).json()
        return Dataset(**response)


    def add_samples(self, experiment, samples=["ALL"]):
        """Add samples to a dataset

        returns: Dataset

        parameters:

            experiment (str): accession code for the Experiment related to the Samples you
                              are adding to the dataset

            samples (list): list of Sample accession codes for the samples you are adding
                            to the dataset
        """
        if self.is_processing or self.is_processed:
            print("Cannot add samples to a dataset that has been processed!")
            return

        if self.data:
            self.data = {**self.data, experiment: samples}
        else:
            self.data = {experiment: samples}

        return self



    def save(self):
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

        return Dataset(**response)


    def process(self):
        self.start = True
        response = self.save()
        self.is_processing = response.is_processing


    def check(self):
        response = self.get(self.id)
        self.is_processing = response.is_processing
        self.is_processed = response.is_processed
        return response.is_processed


    def download(self, path):
        download_url = self.download_url or self.get(self.id).download_url

        if not download_url:
            raise DownloadError("dataset", "Download url not found - did you process the dataset?")

        download_file(download_url, path)
