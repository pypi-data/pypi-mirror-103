import requests
from open_weather_api.config import Config
from open_weather_api.constants import URL_API

class Api(Config):
    def __init__(self, config):
        print("API")
        print(config)
        print("¡¡API preparada!!")
        super().__init__(config)

    def __get_url(self, find_params):
        """
        Generate URL with all data
        ---------------------------
        Use find params (by city or coordinates)
        Metric o default units system
        Language
        """
        lang = self.get_lang()
        units = self.get_units()
        params = f"{find_params}{lang}{units}"
        type = self.get_type()
        api_key = self.get_api_key()
        # print(f'{URL_API}{type}{params}{api_key}')
        return f'{URL_API}{type}{params}{api_key}'
    
    def get_data(self, find_params):
        """ Create API request URL to take want data"""
        return requests.get(self.__get_url(find_params)).json()
        