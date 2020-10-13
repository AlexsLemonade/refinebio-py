import logging
import os

import requests

logger = logging.getLogger(__name__)

base_url = os.getenv("BASE_URL") or "https://api.refine.bio/v1/"


def request(method, url, params=None, payload=None):
    try:
        response = requests.request(method, url, params=params, data=payload)
        response.raise_for_status()
        return response.json()

    except requests.exceptions.HTTPError as http_error:
        response_body = response.json()
        try:
            error_type = response_body["error_type"]
            message = response_body["detail"]

            if error_type == "invalid_filters":
                invalid_filters = response_body["invalid_filters"]
                raise Exception("you have provided invalid filters: {0}".format(invalid_filters))

        except (ValueError, KeyError):
            raise Exception(response_body)

def get(url, params=None):
    return request("GET", url, params=params)


def post(url, payload=None):
    return request("POST", url, payload=payload)


def put(url, payload=None):
    return request("PUT", url, payload=payload)


def get_by_endpoint(endpoint, params=None):
    url = base_url + endpoint + "/"
    return get(url, params=params)


def post_by_endpoint(endpoint, payload=None):
    url = base_url + endpoint + "/"
    return post(url, payload=payload)


def put_by_endpoint(endpoint, payload=None):
    url = base_url + endpoint + "/"
    return put(url, payload=payload)
