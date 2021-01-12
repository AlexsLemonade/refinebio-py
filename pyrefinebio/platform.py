from pyrefinebio.http import get_by_endpoint


class Platform:
    """Platform.

    Retrieve a list of Platforms based on filters

        >>> import pyrefinebio
        >>> og_files = pyrefinebio.Platform.search()
    """

    def __init__(
        self,
        platform_accession_code=None,
        platform_name=None
    ):
        self.platform_accession_code = platform_accession_code
        self.platform_name = platform_name

    @classmethod
    def search(cls, **kwargs):
        """Retrieve a list of Platforms

        Returns:
            list of Platform

        Since there are no filters, this method always returns all Platforms
        """
        response = get_by_endpoint("platforms", params=kwargs).json()
        return [Platform(**platform) for platform in response]
