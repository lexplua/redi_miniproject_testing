"""
1. Which Unit Tests Should Be Created?
    For the SettingsManager class, you should create the following unit tests to ensure each method and behavior works as expected:

    Test Initialization:

    Verify that the SettingsManager object is properly instantiated with a given name.
        Test initial_settings():

    Ensure that the input directories are stored correctly in the settings file.
        Test set_option() and get_option():

    Test that options (such as result directory and input directories) are correctly set and retrieved from the settings.
        Test files_path Property:

    Ensure that the files_path property correctly retrieves and converts the input directories to pathlib.Path objects.
        Test result_path Property:

    Verify that the result_path property retrieves the result directory and defaults to the current directory when not set.
        Test store_config():

    Check if settings are correctly written to the file after changes.
        Test read_config():

    Validate if the settings file is read correctly and returns the expected data.


2. Scenarios Should Be Covered:
    Each test should cover positive and edge case scenarios:

    2.1. Initialization:
        Positive Test: Ensure that the object is instantiated with the correct name.
        Edge Case: Instantiating without a valid name (empty string or None).
    2.2. Settings Manipulation (set_option, get_option, initial_settings):
        Positive Tests:
            Setting and getting valid options like input directories and result directory.
            Initializing input directories with multiple paths.
        Edge Cases:
            Fetching a non-existing option (should return None).
            Setting a value to None (should behave appropriately).
    2.3. Properties (files_path, result_path):
        Positive Tests:
            files_path: Ensure input directories are correctly converted to pathlib.Path.
            result_path: Ensure result directory is fetched or defaults to the current directory.
        Edge Cases:
            When input_dirs is not set (should return an empty list).
            When result_dir is not set (should return current directory).
    2.4. File Handling (read_config, store_config):
        Positive Tests:
            Verify settings are read from and written to the correct file.
        Edge Cases:
            What happens if the file doesn't exist yet (should handle file creation).
            Test behavior with a malformed JSON file.
3. What Kind of Fixtures Should Be Created?
    Fixtures are useful to provide controlled environments and data for your tests.
    For this code, the following fixtures are recommended:

    Temporary Directory Fixture:

    A fixture to create a temporary directory for settings JSON files so that the actual file system isn’t affected during testing.
        You can use https://docs.pytest.org/en/stable/how-to/tmp_path.html
    Mock Settings File Fixture:
        A fixture to create and mock a settings.json file with predefined data for testing reading and writing functionality.
"""
import pathlib
from collections.abc import Iterable
from json import JSONDecodeError
from unittest.mock import patch

import pytest

from miniproject import SettingsManager, SettingKey

mock_input_dirs_json = {"input_dirs": ["input/dir1", "input/dir2"]}

mock_input_dirs = [pathlib.Path("./input/dir1"), pathlib.Path("./input/dir2")]

mock_input_dirs_none = [None, None]

mock_names = ["Gena", "Markus"]


malformed_json_data = '''{
    "name": "John",
    "age": 30,
}'''


@pytest.fixture
def settings_manager(tmp_path):
    mock_settings_path = tmp_path / "settings.json"

    with patch('miniproject.get_settings_path', return_value=mock_settings_path):
        yield SettingsManager("test")


def test_initial_settings(settings_manager):
    settings_manager.initial_settings(mock_input_dirs)
    assert settings_manager.read_config() == mock_input_dirs_json


def test_initial_settings_none(settings_manager):
    with (pytest.raises(TypeError)):
        assert settings_manager.initial_settings(None)


@pytest.mark.parametrize(
    "elements, expected",
    [
        (["Gena", "Markus"], ["Gena", "Markus"]),
        (["Markus"], ["Markus"]),
        ("Markus", "Markus"),
        ("NonExistingOption", None),
        (None, None)
    ]
)
def test_options(settings_manager, elements, expected):
    if isinstance(elements, Iterable) and not isinstance(elements, str):
        settings_manager.set_option(SettingKey.INPUT_DIRS.NAME.value, [str(p) for p in elements])
    else:
        settings_manager.set_option(SettingKey.INPUT_DIRS.NAME.value, elements)
    if elements == "NonExistingOption":
        assert settings_manager.get_option(elements) == expected
    else:
        assert settings_manager.get_option(SettingKey.INPUT_DIRS.NAME.value) == expected


def test_files_path(settings_manager):
    settings_manager.initial_settings(mock_input_dirs)
    assert settings_manager.files_path == mock_input_dirs


def test_result_path(settings_manager):
    result_dir = "./output/results"
    settings_manager.set_option(SettingKey.RESULT_DIR.value, result_dir)
    assert settings_manager.result_path == pathlib.Path("./output/results")


def test_paths_none(settings_manager):
    settings_manager.set_option(SettingKey.INPUT_DIRS.NAME.value, [str(p) for p in mock_names])
    print(settings_manager.read_config())
    print(settings_manager.result_path)
    assert settings_manager.files_path == []
    assert settings_manager.result_path == pathlib.Path(".")


def test_store_config(settings_manager):
    settings_manager.store_config(mock_input_dirs_json)
    assert settings_manager.read_config() == mock_input_dirs_json


def test_file_is_not_created(settings_manager):
    with (pytest.raises(FileNotFoundError)):
        settings_manager.read_config()


def test_malformed_json_data(settings_manager):
    if not settings_manager.settings_path.parent.exists():
        settings_manager.settings_path.parent.mkdir(exist_ok=True)
    with open(settings_manager.settings_path, "w") as settings_file:
        settings_file.write(malformed_json_data)
    with (pytest.raises(JSONDecodeError)):
        settings_manager.read_config()

