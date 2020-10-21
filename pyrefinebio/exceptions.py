
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
            self.base_message += ": " + message
        super().__init__(self.base_message)

class NotFound(Exception):
    base_message = "The requested resource at {0} was not found"
    def __init__(self, url):
        super().__init__(self.base_message.format(url))


class InvalidFilters(Exception):
    base_message = "You have provided invalid filters: {0}"
    def __init__(self, invalid_filters):
        super().__init__(self.base_message.format(invalid_filters))