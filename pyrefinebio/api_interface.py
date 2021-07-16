import json
import shutil

import requests
from pyrefinebio.config import Config
from pyrefinebio.exceptions import (
    BadRequest,
    InvalidData,
    InvalidFilters,
    InvalidFilterType,
    MultipleErrors,
    NotFound,
    ServerError,
)
from requests.exceptions import ConnectionError


def request(method, url, params=None, payload=None):
    try:
        config = Config()
        headers = {"Content-Type": "application/json", "API-KEY": config.token}

        if payload:
            payload = json.dumps(payload)

        response = requests.request(method, url, params=params, data=payload, headers=headers)
        response.raise_for_status()

        return response

    except requests.exceptions.HTTPError as e:
        code = response.status_code
        response_body = response.json()

        if code == 400:
            error = _handle_error(response_body)
            raise error

        elif code == 404:
            raise NotFound(response.url)

        elif code == 500:
            raise ServerError()

        else:
            print(response_body)
            raise e
    except ConnectionError:
        raise ServerError()


def get(url, params=None):
    return request("GET", url, params=params)


def post(url, payload=None):
    return request("POST", url, payload=payload)


def put(url, payload=None):
    return request("PUT", url, payload=payload)


def get_by_endpoint(endpoint, params=None):
    config = Config()
    url = config.base_url + endpoint + "/"
    return get(url, params=params)


def post_by_endpoint(endpoint, payload=None):
    config = Config()
    url = config.base_url + endpoint + "/"
    return post(url, payload=payload)


def put_by_endpoint(endpoint, payload=None):
    config = Config()
    url = config.base_url + endpoint + "/"
    return put(url, payload=payload)


def download_file(url, path, prompt):
    with requests.get(url, stream=True) as res:

        if prompt:
            total_size_in_bytes = int(res.headers.get("content-length", -1))
            message = None

            if total_size_in_bytes == -1:
                message = (
                    "Could not get the size for the file you are tying to download. "
                    "Would you still like to download it? (y/N)"
                )
            if total_size_in_bytes > 1024 * 1024 * 1024:
                message = (
                    "The file you are trying to download is bigger than 1GB ({:.2f}GB). "
                    "Would you still like to download it? (y/N)"
                ).format(total_size_in_bytes / (1024 * 1024 * 1024))

            if message:
                yn = input(message)

                if yn.lower() not in ("y", "yes"):
                    return

        with open(path, "wb") as f:
            shutil.copyfileobj(res.raw, f)


def _handle_error(response_body):
    try:
        error_type = response_body["error_type"]
        message = response_body["message"]
        details = response_body["details"]

        if error_type == "multiple_errors":
            return _hanlde_multiple_errors(details)

        if error_type == "invalid_filters":
            return InvalidFilters(details)

        if error_type == "invalid_data":
            return InvalidData(message, details)

        if error_type == "invalid" or error_type == "invalid_choice":
            return InvalidFilterType(details, message)

        return BadRequest(message)

    except (ValueError, KeyError, TypeError):
        return BadRequest(response_body)


def _hanlde_multiple_errors(errors):
    exceptions = []

    for error in errors:
        exceptions.append(_handle_error(error))

    return MultipleErrors(exceptions)
