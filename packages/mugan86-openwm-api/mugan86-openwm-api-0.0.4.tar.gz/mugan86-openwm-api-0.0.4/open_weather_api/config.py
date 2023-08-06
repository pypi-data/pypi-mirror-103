class Config:

    def __init__(self, config):
        print('Iniciando config')
        self.set_api_key(config['key'])
        self.set_units(config['units'])
        self.set_lang(config['lang'])
        self.set_type(config['type'])

    def set_api_key(self, api_key):
        if (api_key == None or api_key == ''):
            raise ValueError('Need add API Key please.')
        self.__api_key = f'&appid={api_key}'

    def get_api_key(self):
        return self.__api_key

    def set_units(self, units):
        self.__units = f'&units=metric' if (units == 'm') else ''

    def get_units(self):
        return self.__units

    def set_lang(self, lang):
        if (lang == '' or lang == None): lang = 'es'
        self.__lang = f'&lang={lang}'

    def get_lang(self):
        return self.__lang

    def set_type(self, type):
        if (type == '' or type == None): 
            raise ValueError("Specify type please. 'current' or 'forecast'")
        self.__type = type

    def get_type(self):
        return self.__type
