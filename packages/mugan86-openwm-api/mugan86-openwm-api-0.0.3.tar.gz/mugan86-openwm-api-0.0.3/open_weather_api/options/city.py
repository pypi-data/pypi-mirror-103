from open_weather_api.api import Api

class City(Api):
    
    def __init__(self, city = "", config =  None):
        if (city == ""): raise ValueError("Need add City to take weather")
        if (config == None): raise ValueError("Config add")
        self.set_city(city)
        super().__init__(config)

    def set_city(self, city):
        self.__name = f"q={city}"

    def get_city(self):
        return self.__name

    def get_data(self):
        return super().get_data(self.get_city())