import abc
import pickle
from io import StringIO
from typing import Iterator
from lxml import etree

import requests


class Client(abc.ABC):
    # filename to store/load already visited urls to be overwritten
    file: str = None
    # the url to load the listing of the apartments
    baseurl: str = None

    def __init__(self, **kwargs):
        # data structure holding the already visited urls
        self.visited: set[str] = self._load_visited()
        # a list of urls from the baseurl search
        self.listings: Iterator[str] = []
        # Set explicit HTMLParser
        self.parser = etree.HTMLParser()
        # create a persistent (keep alive) session
        self.session = self._open_session()

    def find_new(self):
        raise NotImplementedError()

    def parse_listings(self, links: tuple[str, str]) -> list[str]:
        raise NotImplementedError()

    def refresh_listings(self):
        try:
            resp = requests.get(self.baseurl)
            resp.raise_for_status()
            # Decode the page content from bytes to string
            html = resp.content.decode("utf-8")
            # Create your etree with a StringIO object which functions similarly to a fileHandler
            tree = etree.parse(StringIO(html), parser=self.parser)
            # This will get the anchor tags <a href...>
            refs = tree.xpath("//a")
        except requests.exceptions.RequestException as e:
            self.logger.error(f"Failed to contact baseurl: {e}")
        except UnicodeDecodeError:
            self.logger.error(f"Failed to decode the html from baseurl: {e}")
        else:
            self.listings = self.parse_listings(refs)

    def exit(self):
        self._save_visited()

    def _load_visited(self):
        try:
            with open(self.file, 'r') as fin:
                visited = pickle.load(fin)
                return visited
        except FileNotFoundError:
            return set()

    def _save_visited(self):
        with open(self.file, 'wx') as fout:
            pickle.dump(self.visited, fout)

    @staticmethod
    def _open_session() -> requests.Session:
        # client's session to persist TCP connetions and cookies
        session = requests.Session()
        session.headers.update({
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; rv:111.0) Gecko/20100101 Firefox/111.0"
        })
        # set proxy
        session.proxies = {
            'http': 'http://localhost:9191',
            'https': 'https://localhost:9191'
        }
        # Ignore TLS/SSL errors
        session.verify=False

        return session
