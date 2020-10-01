from pyrefinebio.http import get_by_endpoint


class Institution:
    """Institution 

    search for institutions

        ex:
        >>> import pyrefinebio
        >>> institutions = pyrefinebio.Institution.search()
    """

    def __init__(self, submitter_institution=None):
        self.submitter_institution = submitter_institution

    @classmethod
    def search(cls):
        """Search for an institution

        returns: list of Institution

        Since there are no filters, this method always gets all institutions.
        """
        response = get_by_endpoint("institutions")
        return [Institution(**institution) for institution in response]
