import logging
import os
import requests
import json

from .exceptions import ServerError, BadRequest, NotFound, InvalidFilters

logger = logging.getLogger(__name__)

base_url = os.getenv("BASE_URL") or "https://api.refine.bio/v1/"


def request(method, url, params=None, payload=None):
    try:
        headers = {
            "Content-Type": "application/json",
            "API-KEY": None
        }
        response = requests.request(method, url, params=params, data=json.dumps(payload), headers=headers)
        response.raise_for_status()
        return response.json()

    except requests.exceptions.HTTPError:
        code = response.status_code
        response_body = response.json()

        if code == 400:
            try:
                error_type = response_body["error_type"]
                message = response_body["detail"]

                if error_type == "invalid_filters":
                    invalid_filters = response_body["invalid_filters"]
                    raise InvalidFilters(invalid_filters)

                raise BadRequest(message)

            except (ValueError, KeyError):
                raise BadRequest(response_body)
        
        elif code == 404:
            raise NotFound(response.url)

        elif code == 500:
            raise ServerError

        else:
            print(response_body)
            raise Exception("An unexpected error has occured")


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
