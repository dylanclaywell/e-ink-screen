import requests
from logger import Logger

class Services:
    @staticmethod
    def get(url):
        Logger.debug(f"Fetching {url}")

        response = requests.get(url)

        if response.status_code == 200:
            content_type = response.headers.get('Content-Type')

            
            if 'application/json' in content_type:
                data = response.json()
            else:
                data = response.content

            Logger.info(f"Fetched {url}: {data}")
            return data
        else:
            Logger.info(f"Error fetching {url}: {response.status_code}")
            return None

