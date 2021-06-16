from pyrefinebio.api_interface import get_by_endpoint
from pyrefinebio.base import Base


class Institution(Base):
    """Institution

    Retrieve a list of Institutions

        >>> import pyrefinebio
        >>> institutions = pyrefinebio.Institution.search()
    """

    def __init__(self, submitter_institution=None):
        self.submitter_institution = submitter_institution

    @classmethod
    def search(cls):
        """Retrieve a list of Institutions

        Returns:
            list of Institution

        Since there are no filters, this method always gets all Institutions.
        """
        response = get_by_endpoint("institutions").json()
        return [Institution(**institution) for institution in response]
