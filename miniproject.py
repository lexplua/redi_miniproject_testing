import json
import pathlib
from enum import Enum
from typing import List


class SettingKey(Enum):
    RESULT_DIR = "result_dir"
    INPUT_DIRS = "input_dirs"
    NAME = "name"


def get_settings_path() -> pathlib.Path:
    # Return default filepath for settings
    return pathlib.Path("./files/settings.json")


class SettingsManager:
    def __init__(self, name: str):
        self.name = name
        self.settings_path = get_settings_path()

    @property
    def files_path(self) -> List[pathlib.Path]:
        return [pathlib.Path(path) for path in self.get_option("input_dirs")]

    @property
    def result_path(self) -> pathlib.Path:
        return pathlib.Path(self.get_option("result_dir") or ".")

    def set_option(self, key, value):
        # Creates or updates settings in the config file

        if self.settings_path.exists():
            with open(self.settings_path) as settings_file:
                settings = json.load(settings_file)
        else:
            settings = {}
        settings[key] = value
        self.store_config(settings)

    def store_config(self, settings: dict):
        # Writes dictionary with settings to JSON file

        if not self.settings_path.parent.exists():
            self.settings_path.parent.mkdir(exist_ok=True)
        with open(self.settings_path, "w") as settings_file:
            json.dump(settings, settings_file, indent=4)

    def get_option(self, key):
        # Reads config file and returns value from this file
        settings = self.read_config()
        return settings.get(key)

    def read_config(self):
        with open(self.settings_path, "r") as settings_file:
            settings = json.load(settings_file)
        return settings

    def initial_settings(self, input_dirs):
        self.set_option(SettingKey.INPUT_DIRS.value, [str(p) for p in input_dirs])


