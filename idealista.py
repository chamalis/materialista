import logging
import time

import selenium.common.exceptions
from selenium.webdriver.common.by import By

import settings
from cli import Client


class IdealistaClient(Client):
    baseurl = """
    https://www.idealista.com/en/alquiler-viviendas/{province}-{city}/
    con-precio-hasta_{max_price},precio-desde_{min_price},
    metros-cuadrados-mas-de_{min_surface},metros-cuadrados-menos-de_{max_surface}
    """
    # baseurl = "https://www.idealista.com/en/alquiler-viviendas/barcelona-barcelona"
    file = "idea.pickle"
    outfile = "ideares.txt"
    next_page_xpath = "/html/body/div[2]/div/div/main/section/div/ul/li[8]/a"

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.baseurl.format(
            province=settings.PROVINCE,
            city=settings.CITY,
            max_price=settings.MAX_PRICE,
            min_price=settings.MIN_PRICE,
            min_surface=settings.MIN_SURFACE,
            max_surface=settings.MAX_SURFACE
        )

    def parse_listings(self) -> list[str]:
        ret = []

        while True:
            time.sleep(2)

            elems = self.client.find_elements(by=By.XPATH, value="//a[@href]")
            for elem in elems:
                l = elem.get_attribute("href")
                if l and "/inmueble/" in l and l not in self.visited:
                    ret.append(l)

            time.sleep(8)
            try:
                next_page_elem = self.client.find_element(By.XPATH, self.next_page_xpath)
            except selenium.common.exceptions.NoSuchElementException:
                break
            else:
                href = next_page_elem.get_attribute('href')
                self.client.get(href)

        return ret

    def find_new(self):
        # refresh_listings will call parse_listings
        self.refresh_listings()

        for u in self.new_aparts:
            time.sleep(1)
            self.client.get(u)

            html = self.client.page_source.lower()  # str
            if "muchas peticiones" in html or "many requests" in html:
                self.logger.error("robot activity detected... exiting...")
                self.exit(1)

            if (
                    (
                         "1 month deposit" in html
                         or "no agency" in html
                         or "private owner" in html
                    ) and (
                        not "3 month deposit" in html
                    )
            ):
                self.trgt_aparts.append(u)
            self.visited.add(u)

        print(f"found {len(self.trgt_aparts)} new apartements to visit:")
        for a in self.trgt_aparts:
            print(a)


