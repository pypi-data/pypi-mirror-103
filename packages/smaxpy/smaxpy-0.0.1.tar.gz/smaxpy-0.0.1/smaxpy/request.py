from __future__ import annotations

import requests
import cloudscraper
from requests.models import Response

from .errors import RequestError


def request_wrapper(website: str, headers: dict) -> Response:
    """
    Just a simple wrapper for the `requests` module.
    """
    try:
        r = requests.get(website, headers=headers)
    except Exception:
        raise RequestError(
            "There was a problem with your request, please try again later."
        )

    return r


def cfscrape_wrapper(website: str) -> Response:  # , allow_brotli: bool = True
    """
    Just a simple wrapper for the `cloudscraper` module.
    """

    # TODO: better implementation

    scraper = cloudscraper.create_scraper()

    try:
        r = scraper.get(website)
    except Exception:
        raise RequestError(
            "There was a problem with your request, please try again later."
        )

    return r