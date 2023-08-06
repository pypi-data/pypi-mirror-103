class ConfigReaderManager:
    def __init__(self, config_reader: callable):
        self.__config_reader = config_reader

    def set_config_reader(self, config_reader: callable):
        self.__config_reader = config_reader

    @property
    def config_reader(self):
        return self.__config_reader
