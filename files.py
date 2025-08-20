import os
from PIL import Image
from io import BytesIO
from logger import Logger

code_lut = {
    "01d": "clear-day",
    "01n": "clear-night",
    "02d": "cloudy-day",
    "02n": "cloudy-night",
    "03d": "cloudy",
    "03n": "cloudy",
    "04d": "cloudy",
    "04n": "cloudy",
    "09d": "rain",
    "09n": "rain",
    "10d": "rain",
    "10n": "rain",
    "11d": "thunderstorm",
    "11n": "thunderstorm",
    "13d": "snow",
    "13n": "snow",
    "50d": "mist",
    "50n": "mist",
}

class Files:

    @staticmethod
    def create_dir(d):
        if not os.path.exists(d):
            os.makedirs(d)

    @staticmethod
    def create_external_dir():
        Files.create_dir('./external')

    @staticmethod
    def load_weather_img(code):
        mapping = code_lut.get(code)

        if mapping is None:
            return None

        path = f"./assets/weather/{mapping}.png"

        if not os.path.exists(path):
            return None

        return Image.open(path)

