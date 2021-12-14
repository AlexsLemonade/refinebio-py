from pyrefinebio import organism as prb_organism
from pyrefinebio.api_interface import get_by_endpoint
from pyrefinebio.base import Base
from pyrefinebio.util import parse_date


class QNTarget(Base):
    """QN Target.

    Retrieve a QN target by organism name

        >>> import pyrefinebio
        >>> organism_name = "GORILLA"
        >>> qn_target = pyrefinebio.QNTarget.get(organism_name)

    Retrieve a list of QN target organisms

        >>> import pyrefinebio
        >>> qn_target_organisms = pyrefinebio.QNTarget.search()
    """

    def __init__(
        self,
        id=None,
        filename=None,
        size_in_bytes=None,
        is_qn_target=None,
        sha1=None,
        s3_bucket=None,
        s3_key=None,
        s3_url=None,
        created_at=None,
        last_modified=None,
        result=None,
    ):
        super().__init__(identifier=id)

        self.id = id
        self.filename = filename
        self.size_in_bytes = size_in_bytes
        self.is_qn_target = is_qn_target
        self.sha1 = sha1
        self.s3_bucket = s3_bucket
        self.s3_key = s3_key
        self.s3_url = s3_url
        self.created_at = parse_date(created_at)
        self.last_modified = parse_date(last_modified)
        self.result = result

    @classmethod
    def get(cls, organism_name):
        """Retrieve a QNTarget based on organism name

        Returns:
            QNTarget

        Parameters:
            organism_name (str): the name of the organism for the QNTarget you want to get
        """
        response = get_by_endpoint("qn_targets/" + organism_name).json()
        return QNTarget(**response)

    @classmethod
    def search(cls, **kwargs):
        """Retrieve a list of Organisms that have available QNTargets

        Returns:
            list of Organism

        Since there are no filters, this method always returns all Organisms that have available QNTargets
        """
        response = get_by_endpoint("qn_targets", params=kwargs).json()
        return [prb_organism.Organism(**qn_organism) for qn_organism in response]
