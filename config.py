class Config:
    def __init__(self, config):
        self.config = config

    def getWaveshareDirectory(self):
        waveConfig = self.config.get('waveshare')
        if waveConfig is None:
            print('Waveshare entry missing from config; please check config.yaml')
            exit()

        waveDir = waveConfig.get('dir')
        if waveDir is None:
            print('Waveshare directory missing from config; please check config.yaml')
            exit()

        return waveDir

    def getWeatherConfig(self):
        weatherConfig = self.config.get('weather')

        if weatherConfig is None:
            print('Weather entry missing from config; please check config.yaml')
            exit()

        apiKey = weatherConfig.get('apiKey')

        if apiKey is None:
            print('Weather API key missing from config; please check config.yaml')
            exit()

        locations = weatherConfig.get('locations')

        return apiKey, locations
