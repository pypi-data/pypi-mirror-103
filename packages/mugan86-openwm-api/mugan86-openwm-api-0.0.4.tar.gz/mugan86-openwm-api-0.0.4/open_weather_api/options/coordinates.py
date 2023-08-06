from open_weather_api.api import Api
class Coordinates(Api):
    def __init__(self, location='', config=None):
        if (location == '' or location == None): 
            raise ValueError("Need add Coordinates to take weather")
        if (config == None): raise ValueError("Config add")
        self.set_location(location)
        super().__init__(config)

    def set_location(self, location):
        lat_lon = str(location).split(',')
        self.__location = f"lat={lat_lon[0]}&lon={lat_lon[1]}"

    def get_location(self):
        return self.__location

    def get_data(self):
        return super().get_data(self.get_location())