import logging
import pathlib

from miniproject import SettingsManager, SettingKey

# Setting up logging configuration
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')


def demo_settings_manager():
    # Create an instance of SettingsManager with a name, e.g., 'student1'
    name = "student1"
    manager = SettingsManager(name=name)

    # Initialize settings: specifying input directories
    input_dirs = [pathlib.Path("./input/dir1"), pathlib.Path("./input/dir2")]
    logging.info("Initializing input directories...")
    manager.initial_settings(input_dirs)

    # Set the result directory
    result_dir = "./output/results"
    logging.info("Setting result directory...")
    manager.set_option(SettingKey.RESULT_DIR.value, result_dir)

    # Retrieve and print the input directories
    input_paths = manager.files_path
    logging.info("Retrieved input directories: %s", input_paths)

    # Retrieve and print the result directory
    result_path = manager.result_path
    logging.info("Retrieved result directory: %s", result_path)

    # Fetching a non-existing option to demonstrate fallback behavior
    name = manager.get_option(SettingKey.NAME.value)
    if name is None:
        logging.warning("Name is not set in the settings.")
    else:
        logging.info("Name: %s", name)


if __name__ == "__main__":
    demo_settings_manager()
