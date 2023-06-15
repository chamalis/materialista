import abc
import logging
import os
import pickle
import sys
import time
# importing date class from datetime module
from datetime import date

import requests
from lxml import etree
from selenium import webdriver


class Client(abc.ABC):
    # filename to store/load already visited urls to be overwritten
    file: str = None
    # the url to load the listing of the apartments
    baseurl: str = None
    # the output filename (abs path) to save results
    outfile: str = None

    def __init__(self, **kwargs):
        # create a logger with the instance's class name
        self.logger = logging.getLogger(self.__class__.__name__)
        # data structure holding the already visited urls
        self.visited: set[str] = self._load_visited()
        # a list of new urls from the baseurl search
        self.new_aparts: list[str] = []
        # a sub list of the above which fit our requirements
        self.trgt_aparts: list[str] = []
        # Set explicit HTMLParser
        self.parser = etree.HTMLParser()
        # create a persistent (keep alive) session
        self.client = self._open_session()

    def find_new(self):
        raise NotImplementedError()

    def parse_listings(self) -> list[str]:
        raise NotImplementedError()

    def refresh_listings(self):
        time.sleep(2)

        try:
            self.client.get(self.baseurl)
            # self.driver.find_element_by_id("nav-search").send_keys("Selenium")
        except requests.exceptions.RequestException as e:
            self.logger.error(f"Failed to contact baseurl: {e}")
        except UnicodeDecodeError:
            self.logger.error(f"Failed to decode the html from baseurl: {e}")
        else:
            # self.new_aparts = self.parse_listings(refs)
            self.new_aparts = self.parse_listings()

    def exit(self, status: int):
        self.print_results()
        self._save_visited()
        self.client.close()

        sys.exit(status)

    def print_results(self):
        # creating the date object of today's date
        todays_date = str(date.today())

        with open(self.outfile, "a") as fout:
            fout.write("\n\n")
            fout.write("---===" * 5 + todays_date + "---===" * 5 + "\n")
            for u in self.trgt_aparts:
                fout.writelines([u, '\n'])
            fout.write("---===" * 5 + todays_date + "---===" * 5 + "\n")

    def _load_visited(self) -> set[str]:
        ret: set[str] = set()

        try:
            if os.path.getsize(self.file) > 4:
                with open(self.file, 'rb') as fin:
                    ret = pickle.load(fin)
        except FileNotFoundError:
            print(f"Warning: {self.file} was not found")

        return ret

    def _save_visited(self):
        with open(self.file, 'wb') as fout:
            pickle.dump(self.visited, fout)
        self.client.close()

    @staticmethod
    def _open_session() -> webdriver.Firefox:
        driver = webdriver.Firefox()

        return driver
