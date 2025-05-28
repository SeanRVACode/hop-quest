import requests
import yaml
from icecream import ic
from .utilities import Data_Cleaner
from urllib.parse import urlencode


# Load the config file that stores values needed for API
with open("./app/services/config.yaml") as file:
    cfg = yaml.load(file, Loader=yaml.FullLoader)


class Brew_Service:
    def __init__(self):
        self.dc = Data_Cleaner()
        self.base_url = cfg["openbrewery"]["base_url"]
        self.session = requests.Session()
        ic(self.base_url)

    def random_breweries(self):
        data = self._get_ten_random_breweries()
        ic("Random Brew Search")
        updatated_data = self.dc.create_map_link(data)
        return updatated_data

    def _get_ten_random_breweries(self):
        # TODO look into time out to prevent hanging
        url = f"{self.base_url}/random?size=10"

        try:
            response = self.session.get(url)

            response.raise_for_status()

            # Convert response to json data
            data = response.json()

            return data

        except Exception as e:
            ic(e)
            raise Exception


if __name__ == "__main__":
    Brew_Service()
