import requests
from services import Services
from logger import Logger
from files import Files

class OpenWeather:
    def __init__(self, apiKey, locations):
        self.apiKey = apiKey
        self.locations = []

    def find_lat_lon(self, location):
        url = f"https://api.openweathermap.org/geo/1.0/direct?q={location.get('query')}&limit=1&appid={self.apiKey}"

        Logger.debug(f"Fetching lat and lon for {location.get('name')}: {url}")

        response = Services.get(url)
        Logger.debug(f"Fetched lat and lon: {response}")
        loc = response[0]
            
        if loc is None:
            Logger.debug(f"Error fetching lat and lon for {location.get('name')}: Location not found")
            return None

        return {
            "lat": loc.get('lat'),
            "lon": loc.get('lon'),
        }

    def get_lat_lon_weather(self, lat, lon):
        url = f"https://api.openweathermap.org/data/2.5/weather?lat={lat}&lon={lon}&appid={self.apiKey}"

        Logger.debug(f"Fetching weather data for lat {lat} and lon {lon}: {url}")

        response = Services.get(url)

        Logger.debug(f"Fetched weather data: {response}")
            
        return response

    def poll_location(self, id):
        location = list(filter(lambda loc: loc.get('id') == id, self.locations))[0]

        if location is None:
            Logger.debug(f"Error polling location: {id} does not exist in registered locations")
            return

        latLon = self.find_lat_lon(location)

        return self.get_lat_lon_weather(latLon.get('lat'), latLon.get('lon'))

    def add_location(self, location):
        self.locations.append(location)

    def get_weather_code_img(self, code):
        img = Files.load_weather_img(code)

        return img.convert("RGBA")
