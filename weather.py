import requests
from services import Services
from logger import Logger
from files import Files
from PIL import Image, ImageDraw, ImageFont
from datetime import datetime

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

        return loc

    def get_lat_lon_weather(self, lat, lon):
        url = f"https://api.openweathermap.org/data/2.5/weather?lat={lat}&lon={lon}&appid={self.apiKey}&units=imperial"

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

        return self.get_lat_lon_weather(latLon.get('lat'), latLon.get('lon')), latLon

    def add_location(self, location):
        self.locations.append(location)

    def get_weather_code_img(self, code):
        img = Files.load_weather_img(code)

        return img.convert("RGBA")

    def draw_center(self, pos, draw, font, message):
        _, _, w, h = draw.textbbox((0, 0), message, font=font)
        draw.text((pos[0]-(w/2), pos[1]), message, font=font)

    def draw_pair(self, pos, draw, font, v1, v2):
        self.draw_center(pos, draw, font, v1)
        self.draw_center((pos[0], pos[1]+12), draw, font, v2)

    def draw(self, image):
        curWeather, latLon = self.poll_location('fishers')

        city = latLon.get("name")
        state = latLon.get("state")

        temp = round(curWeather.get('main').get('temp'))

        feelsLike = round(curWeather.get('main').get('feels_like'))
        humidity = curWeather.get('main').get('humidity')
        pressure = round(curWeather.get('main').get('pressure'))
        seaLevel = round(curWeather.get('main').get('sea_level'))

        cur_date = datetime.now()
        day = cur_date.strftime("%A")
        month = cur_date.strftime("%B")
        date = cur_date.day

        weatherImage = self.get_weather_code_img(curWeather.get('weather')[0].get('icon'))

        image.paste(weatherImage, (2, 48), weatherImage)

        weatherFontHeading = ImageFont.truetype("./assets/fonts/Roboto-Regular.ttf", 16)
        weatherFontDate = ImageFont.truetype("./assets/fonts/Roboto-Regular.ttf", 12)
        weatherFontTemp = ImageFont.truetype("./assets/fonts/Roboto-Thin.ttf", 24)

        draw = ImageDraw.Draw(image)
        
        self.draw_center((250 / 2, 8), draw, weatherFontHeading, f"{city}, {state}")

        self.draw_center((250 / 2, 32), draw, weatherFontDate, f"{day}, {month} {date}")

        self.draw_center((88, 64), draw, weatherFontTemp, f"{temp}")
        _, _, tempW, tempH = draw.textbbox((0, 0), f"{temp}", font=weatherFontTemp)

        draw.text((88 + (tempW/2) + 2, 64 + 3), "°F", font=weatherFontDate)

        self.draw_pair((158, 54), draw, weatherFontDate, "Feels like", f"{feelsLike}")
        self.draw_pair((158, 54 + 28), draw, weatherFontDate, "Humidity", f"{humidity}%")

        self.draw_pair((214, 54), draw, weatherFontDate, "Pressure", f"{pressure}hPa")
        self.draw_pair((214, 54 + 28), draw, weatherFontDate, "Sea Level", f"{seaLevel}hPa")

