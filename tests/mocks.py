from requests.exceptions import HTTPError

class MockResponse:
    def __init__(self, json_data, url, status=200, headers=None):
        self.json_data = json_data
        self.url = url
        self.status_code = status
        self.headers = headers

    def json(self):
        return self.json_data
    
    def raise_for_status(self):
        if self.status_code != 200:
            raise HTTPError
