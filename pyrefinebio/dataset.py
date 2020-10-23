from pyrefinebio.http import get_by_endpoint, post_by_endpoint, put_by_endpoint, download_file
from pyrefinebio.exceptions import DownloadError

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
        self.expires_on = expires_on
        self.s3_bucket = s3_bucket
        self.s3_key = s3_key
        self.success = success
        self.failure_reason = failure_reason
        self.created_at = created_at
        self.last_modified = last_modified
        self.start = start
        self.size_in_bytes = size_in_bytes
        self.sha1 = sha1
        self.quantile_normalize = quantile_normalize
        self.quant_sf_only = quant_sf_only
        self.svd_algorithm = svd_algorithm
        self.download_url = download_url


    @classmethod
    def get(cls, id):
        response = get_by_endpoint("dataset/" + id)
        return Dataset(**response)


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
            response = put_by_endpoint("dataset/" + self.id, payload=body)
        else:
            response = post_by_endpoint("dataset", payload=body)

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
            raise DownloadError()

        download_file(download_url, path)
