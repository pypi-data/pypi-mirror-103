import os
from injecta.container.ContainerInterface import ContainerInterface
from pyfonycore.bootstrap.config.Config import Config
from daipecore.bootstrap.config_reader_manager import config_reader_manager


class ContainerManager:

    _container: ContainerInterface

    @classmethod
    def set_container(cls, container: ContainerInterface):
        cls._container = container

    @classmethod
    def get_container(cls):
        if not hasattr(cls, "_container"):
            cls._container = cls._create_container()

        return cls._container

    @staticmethod
    def _create_container():
        bootstrap_config: Config = config_reader_manager.config_reader()

        if "APP_ENV" not in os.environ:
            raise Exception(f"Set APP_ENV env variable to define environment ({', '.join(bootstrap_config.allowed_environments)})")

        return bootstrap_config.container_init_function(os.environ["APP_ENV"], bootstrap_config)
