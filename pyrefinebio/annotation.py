from pyrefinebio.base import Base

from pyrefinebio.util import parse_date


class Annotation(Base):
    def __init__(
        self,
        id=None,
        data=None,
        is_ccdl=None,
        created_at=None,
        last_modified=None
    ):
        self.id = id
        self.data = data
        self.is_ccdl = is_ccdl
        self.created_at = parse_date(created_at)
        self.last_modified = parse_date(last_modified)
