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