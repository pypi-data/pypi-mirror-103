from injecta.package.path_resolver import resolve_path
from pyfonybundles.Bundle import Bundle
from pyfonycore.bootstrap.config.Config import Config

from daipecore.bootstrap.config_reader_manager import config_reader_manager


class DaipeCore(Bundle):
    def modify_raw_config(self, raw_config: dict) -> dict:
        if "daipe" in raw_config["parameters"]:
            raise Exception("parameters.daipe must not be explicitly defined")

        bootstrap_config: Config = config_reader_manager.config_reader()

        raw_config["parameters"]["daipe"] = {
            "root_module": {
                "name": bootstrap_config.root_module_name,
                "path": resolve_path(bootstrap_config.root_module_name).replace("\\", "/"),
            }
        }

        return raw_config
