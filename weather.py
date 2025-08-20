import requests

class OpenWeather:
    def __init__(self, apiKey, locations):
        self.apiKey = apiKey
        self.locations = []

    def find_lat_lon(self, location):
        url = f"https://api.openweathermap.org/geo/1.0/direct?q={location.get('query')}&limit=1&appid={self.apiKey}"

        print(f"Fetching lat and lon for {location.get('name')}: {url}")

        response = requests.get(url)

        if response.status_code == 200:
            data = response.json()
            print("Fetched lat and lon:", data)
            loc = data[0]
            
            if loc is None:
                print(f"Error fetching lat and lon for {location.get('name')}: Location not found")
                return None

            return {
                "lat": loc.get('lat'),
                "lon": loc.get('lon'),
            }
        else:
            print(f"Error fetching lat and lon for {location.get('name')}: {response.status_code}")
            return None

    def get_lat_lon_weather(self, lat, lon):
        url = f"https://api.openweathermap.org/data/2.5/weather?lat={lat}&lon={lon}&appid={self.apiKey}"

        print(f"Fetching weather data for lat {lat} and lon {lon}: {url}")

        response = requests.get(url)

        if response.status_code == 200:
            data = response.json()
            print("Fetched weather data:", data)
            
        else:
            print(f"Error fetching weather data for lat {lat} and lon {lon}: {response.status_code}")


    def poll_location(self, id):
        location = list(filter(lambda loc: loc.get('id') == id, self.locations))[0]

        if location is None:
            print(f"Error polling location: {id} does not exist in registered locations")
            return

        latLon = self.find_lat_lon(location)

        print(latLon)
        self.get_lat_lon_weather(latLon.get('lat'), latLon.get('lon'))

    def add_location(self, location):
        self.locations.append(location)

