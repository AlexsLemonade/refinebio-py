import os

import iso8601
from pyrefinebio.api_interface import get


def create_paginated_list(T, response):
    return PaginatedList(T, response)


def parse_date(date):
    try:
        parsed = None
        parsed = iso8601.parse_date(date)
    finally:
        return parsed


def expand_path(path, filename):
    user_path = os.path.expanduser(path)
    full_path = os.path.abspath(user_path)

    if os.path.isdir(full_path):
        full_path = os.path.join(full_path, filename)

    return full_path


class PaginatedList:
    """PaginatedList

    PaginatedLists are returned by all model class `search` methods that deal
    with paginated api responses. PaginatedLists can be indexed like lists and
    iterated through like generators.
    """

    def __init__(self, T, response):
        self.cur = 0
        self.type = T

        self.base_url = response.url

        json = response.json()

        self.total_items = json["count"]
        self.page_size = len(json["results"])

        max_pages = int(self.total_items / self.page_size) if self.page_size else 0

        self.pages = [None for _ in range(max_pages + 1)]
        self.pages[0] = [T(**item) for item in json["results"]]

    def __getitem__(self, index):

        if isinstance(index, slice):
            step = index.step or 1

            default_start = 0 if step > 0 else self.total_items - 1
            default_stop = self.total_items - 1 if step > 0 else 0

            start = index.start or default_start
            stop = index.stop or default_stop

            if start < 0:
                start += self.total_items

            if stop < 0:
                stop += self.total_items

            if start < 0 or stop < 0:
                raise IndexError("index out of range!")

            return [self[i] for i in range(start, stop, step)]

        if index < 0:
            index += self.total_items

        if index >= self.total_items or index < 0:
            raise IndexError("index out of range!")

        page = int(index / self.page_size)
        page_index = index - page * self.page_size

        try:
            result = self.pages[page][page_index]
        except:
            params = {"offset": page * self.page_size, "limit": self.page_size}

            response = get(self.base_url, params=params).json()

            if self.total_items != response["count"]:
                raise RuntimeError("List has changed since creation!")

            self.pages[page] = [self.type(**item) for item in response["results"]]

            result = self.pages[page][page_index]

        return result

    def __setitem__(self, index, value):
        raise AttributeError("PaginatedLists are immutable")

    def __delitem__(self, index, value):
        raise AttributeError("PaginatedLists are immutable")

    def __len__(self):
        return self.total_items

    def __next__(self):
        if self.cur < self.total_items:
            n = self[self.cur]
            self.cur += 1
            return n
        else:
            raise StopIteration()
