class ServerError(Exception):
    base_message = "The server encountered an issue"
    def __init__(self, message=None):
        if message:
            self.base_message = message
        super().__init__(self.base_message)


class BadRequest(Exception):
    base_message = "Bad Request"
    def __init__(self, message=None):
        if message:
            self.base_message += ": " + str(message)
        super().__init__(self.base_message)


class NotFound(Exception):
    base_message = "The requested resource at {0} was not found"
    def __init__(self, url):
        super().__init__(self.base_message.format(url))


class InvalidFilters(Exception):
    base_message = "You have provided invalid filters: {0}"
    def __init__(self, invalid_filters):
        super().__init__(self.base_message.format(invalid_filters))


class InvalidFilterType(Exception):
    base_message = "You have provided invalid type for the filter, {0} - {1}"
    def __init__(self, filter, info):
        super().__init__(self.base_message.format(filter, info))


class InvalidData(Exception):
    base_message = ""
    def __init__(self, message, details):
        self.base_message = message
        if details:
            self.base_message += "\nDetails: " + str(details)
        super().__init__(self.base_message)


class DownloadError(Exception):
    base_message = "Unable to download dataset"
    def __init__(self):
        super().__init__(self.base_message)


class MultipleErrors(Exception):
    base_message = "Multiple errors have occurred:\n"
    def __init__(self, errors):
        for error in errors:
            self.base_message += str(error) + "\n"
        super().__init__(self.base_message)

