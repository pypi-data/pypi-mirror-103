from daipecore.bootstrap.ConfigReaderManager import ConfigReaderManager
from pyfonycore.bootstrap.config import config_reader

config_reader_manager = ConfigReaderManager(config_reader.read)
