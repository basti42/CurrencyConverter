import requests
from lxml import html

class ConversionRateFetcher():

    def __init__(self, webpage="https://thecurrencycalculator.com/EUR/MYR/"):
        self.webpage = webpage
        self.fetched = False
        self.euroToForeign = float()
        self.foreignToEuro = float()

    def fetch(self):
        try:
            page = html.fromstring(requests.get(self.webpage).content)
            value = page.xpath(".//input[@id='inputTo']")[0].attrib['value']
            self.euroToForeign = float(value)
            self.foreignToEuro = float(1 / self.euroToForeign)
            self.fetched = True

        except BaseException as bex:
            print(bex)
