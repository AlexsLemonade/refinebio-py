

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
        svd_algorithm=None
    ):
        self.id = id
        self.data = data,
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

    @classmethod
    def create(
        cls,
        data,
        aggregate_by=None,
        scale_by=None,
        email_address=None,
        email_ccdl_ok=None,
        start=None,
        quantile_normalize=None,
        quant_sf_only=None,
        svd_algorithm=None
    ):
        pass

    @classmethod
    def get(cls, id):
        pass

    def update(
        self,
        data,
        aggregate_by=None,
        scale_by=None,
        email_address=None,
        email_ccdl_ok=None,
        start=None,
        quantile_normalize=None,
        quant_sf_only=None,
        svd_algorithm=None
    ):
        pass

    def process(self):
        pass

    def check(self):
        pass

    def download(self, path):
        pass