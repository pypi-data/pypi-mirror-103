from __future__ import annotations

from bs4 import BeautifulSoup
from bs4.element import ResultSet

from .request import cfscrape_wrapper, request_wrapper


class Smax:
    def __init__(
        self,
        website: str,
        request_function=None,  # a custom function wrapper
        headers: dict = None,
        cloudflare: bool = False,
    ) -> None:
        # TODO: future better implementation of request_function

        self.website = website
        self.__html = (
            request_function(website).text
            if request_function is not None
            else (
                request_wrapper(website, headers).text
                if not cloudflare
                else cfscrape_wrapper(website, headers).text
            )
        )
        self._soup = BeautifulSoup(self.__html, "lxml")

    def __repr__(self) -> str:
        # TODO: change,
        return "New Smax Class"

    @property
    def title(self) -> str:
        """
        Return the scraped website's title.
        """
        return self._soup.title.get_text()

    @property
    def soup(self) -> BeautifulSoup:
        """
        Return the BeautifulSoup itself.
        """
        return self._soups

    def find_all_links(self, limit: int = None) -> ResultSet:
        """
        Return all links found on the document.
        """
        return self._soup.find_all("a", limit=limit)