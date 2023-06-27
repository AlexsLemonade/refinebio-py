import threading
import time
import unittest
from unittest.mock import patch

import pyrefinebio
from pyrefinebio.exceptions import BadRequest, NotFound
from tests.custom_assertions import CustomAssertions
from tests.mocks import MockResponse


def mock_200_request(method, url, **kwargs):
    experiment = {
        "title": "TEST_EXPERIMENT",
    }
    sample = {
        "accession_code": "TEST_SAMPLE",
    }

    if url == "https://api.refine.bio/v1/experiments/UNDER/":
        experiment["samples"] = [{"accession_code": str(i)} for i in range(9)]
        return MockResponse(experiment, url)

    if url == "https://api.refine.bio/v1/experiments/OVER/":
        experiment["samples"] = [{"accession_code": str(i)} for i in range(10)]
        return MockResponse(experiment, url)

    if url.startswith("https://api.refine.bio/v1/samples/"):
        return MockResponse(sample, url, 200)


def mock_400_request(method, url, **kwargs):
    return MockResponse(
        "we're not home right now", "https://api.refine.bio/v1/organisms/GORILLA", 400
    )


def mock_404_request(method, url, **kwargs):
    return MockResponse(
        "we're not home right now", "https://api.refine.bio/v1/organisms/GORILLA", 404
    )


class ApiInterfaceTests(unittest.TestCase, CustomAssertions):
    PERIOD_SECONDS = 1

    class Timer:
        def __enter__(self):
            self.start = time.time()
            return self

        def __exit__(self, *args, **kwargs):
            self.duration = time.time() - self.start

    @patch("pyrefinebio.api_interface.requests.request", side_effect=mock_400_request)
    def test_400(self, mock_request):
        with self.assertRaises(BadRequest):
            pyrefinebio.Organism.get("GORILLA")

    @patch("pyrefinebio.api_interface.requests.request", side_effect=mock_404_request)
    def test_404(self, mock_request):
        with self.assertRaises(NotFound):
            pyrefinebio.Organism.get("GORILLA")

    @patch("pyrefinebio.api_interface.requests.request", side_effect=mock_200_request)
    def test_rate_limit(self, mock_request):
        time.sleep(self.PERIOD_SECONDS)
        threads = []
        with self.Timer() as timer:
            for sample in pyrefinebio.Experiment.get("UNDER").samples:
                t = threading.Thread(target=lambda: sample.contributed_keywords)
                threads.append(t)
                t.start()
            [t.join() for t in threads]
        self.assertLessEqual(timer.duration, self.PERIOD_SECONDS, timer.duration)

        time.sleep(self.PERIOD_SECONDS)
        threads = []
        with self.Timer() as timer:
            for sample in pyrefinebio.Experiment.get("OVER").samples:
                t = threading.Thread(target=lambda: sample.contributed_keywords)
                threads.append(t)
                t.start()
            [t.join() for t in threads]
        self.assertGreater(timer.duration, self.PERIOD_SECONDS, timer.duration)
