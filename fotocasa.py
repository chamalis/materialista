from cli import Client


class FotoCasaClient(Client):
    baseurl = 'https://www.fotocasa.es/en/rental/homes/barcelona-capital/all-zones/l?maxPrice=4500&minPrice=3500'
    file = 'fotocasa.pickle'

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
