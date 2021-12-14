from pprint import pformat


class Base(object):
    """Base class that all pyrefinebio classes inherit from.

    Contains helpful methods that relate to all classes.
    """

    def __init__(self, identifier=None):
        self._identifier = identifier
        self._fetched = False

    def __str__(self):
        return pformat(self._to_dict())

    def __eq__(self, other):
        try:
            return self._identifier == other._identifier
        except AttributeError:
            return False

    def _to_dict(self):
        expanded = {}

        for key, value in self.__dict__.items():
            if isinstance(value, Base):
                expanded[key] = value._to_dict()
            elif not key.startswith("_"):
                expanded[key] = value

        return expanded

    def __getattribute__(self, attr):
        if (
            not attr.startswith("_")
            and (
                object.__getattribute__(self, attr) is None
                or object.__getattribute__(self, attr) == []
            )
            and not self._fetched
        ):
            # if somehow the identifier isn't set we can't fetch
            # this will only happen with Datasets which can be created by non-api calls
            if self._identifier:
                result = self.get(self._identifier)
                for key, value in result.__dict__.items():
                    setattr(self, key, value)
                self._fetched = True

        return object.__getattribute__(self, attr)
