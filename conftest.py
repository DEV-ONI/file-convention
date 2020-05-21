import os
import shutil
import toml
import pytest
from file_convention.monitor import begin_observer_thread, DirItem

TEST_PATH = './simulated_folder'
DATA_PATH = './tests/data'
TEST_CONFIG = os.path.join(DATA_PATH, 'test_conventions.toml')


def pytest_addoption(parser):
    parser.addini('integration', '')
    parser.addini('basic', '')
    parser.addini('eval', '')
    parser.addini('eval2', '')


def clear_folder():
    """
    clears simulated directory
    """
    for file in os.listdir(TEST_PATH):
        path = os.path.join(TEST_PATH, file)
        if os.path.isdir(path):
            shutil.rmtree(path)
        elif os.path.isfile(path) or os.path.islink(path):
            os.remove(path)
        else:
            pass


@pytest.fixture(scope='function')
def setup_test_folder():
    yield
    clear_folder()


@pytest.fixture(scope='function')
def load_config():
    config_dir = os.path.join(DATA_PATH, 'test_conventions.toml')
    config = toml.load(config_dir)
    print(config)


@pytest.fixture(scope='function')
def folder_creation(setup_test_folder, folder_name):

    folder_path = os.path.join(TEST_PATH, folder_name)
    os.mkdir(folder_path)
    yield folder_path


@pytest.fixture(scope='function')
def file_creation(setup_test_folder, file_name):

    file_path = os.path.join(TEST_PATH, file_name)

    with open(file_path, 'w+'):
        pass

    yield file_path


@pytest.fixture(scope='function')
def batch_file_creation(setup_test_folder, extension_by_folder):

    expected_paths = []

    for folder_name, ext_list in extension_by_folder.items():
        for ext in ext_list:
            file_path = os.path.join(TEST_PATH, 'test_file'+ext)
            expected_path = os.path.join(TEST_PATH, folder_name, 'test_file'+ext)
            with open(file_path, 'w+'):
                expected_paths.append(expected_path)

    yield expected_paths


@pytest.fixture(scope='function')
def observer_thread():

    config = toml.load(TEST_CONFIG)
    dir_handler = DirItem(config)
    observer = begin_observer_thread(dir_handler)

    observer.start()
    yield observer
    observer.stop()
