import logging
from typing import Iterator

import requests as requests

from cli import Client


class IdeaListaClient(Client):
    baseurl = """
    https://www.idealista.com/en/alquiler-viviendas/barcelona-barcelona/con-precio-hasta_1200,precio-desde_850,metros-cuadrados-mas-de_40,metros-cuadrados-menos-de_90,de-un-dormitorio,de-dos-dormitorios,ultimas-plantas,plantas-intermedias/
    """
    file = 'idea.pickle'
    logger = logging.getLogger("idealista.log")

    def parse_listings(self, links: tuple[str, str]) -> Iterator[list[str]]:
        # for l in links:
        #     url = l.get('href', '')
        #     if "/inmueble/" in url:
        #         print(url)
        #         yield url
        urls = [l.get("href") for l in links if "inmueble" in l.get('href', '')]
        return urls

    def find_new(self):
        count = 0
        # refresh listings will call parse_listings to
        url_gen = self.refresh_listings()
        for u in url_gen:
            print(u)
            count += 1
        print(count)

