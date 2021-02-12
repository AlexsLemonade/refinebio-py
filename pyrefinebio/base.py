from pprint import pformat

class Base:
    """Base class that all pyrefinebio classes inherit from.

    Contains helpful methods that relate to all classes.
    """

    def __str__(self):
        return pformat(self._to_dict())


    def _to_dict(self):
        expanded = {}

        for key, value in self.__dict__.items():
            if isinstance(value, Base):
                expanded[key] = value._to_dict()
            else:
                expanded[key] = value

        return expanded

