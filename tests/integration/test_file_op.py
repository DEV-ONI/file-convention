import pytest
import os
import time
import toml
from file_convention.monitor import begin_observer_thread, DirItem

OBSERVER_TIMEOUT = 10

TEST_CONFIG_FILENAME = 'test_conventions.toml'
TEST_PATH = './simulated_folder'


class MockTOML:

    def __init__(self):

        self.target_directory = TEST_PATH
        self.file_sort = dict(
            markdown=['.toml', '.md', '.yaml'],
            video=[
                '.3g2', '.3gp', '.avi',
                '.flv', '.h264', '.m4v',
                '.mkv', '.mov', '.mp4',
                '.mpg', '.rm', '.swf', '.vob', '.wmv'
            ],
            text=[
                '.doc', '.odt', '.pdf',
                '.rtf', '.tex', '.txt', '.wpd'
            ],
            audio=[
                '.aif', '.cda', '.mid',
                '.mp3', '.mpa', '.ogg',
                '.wav', '.wma', '.wpl'
            ],
            compressed_and_executable=[
                '.7z', '.arj', '.deb',
                '.pkg', '.rar', '.rpm',
                '.tar', '.z', '.zip', '.exe'
            ]
        )

    def file_sort_conventions_map(self, *args, **kwargs):
        return {'file_convention': self.file_sort}


# @pytest.mark.eval
@pytest.mark.parametrize('folder_name, expected_result', [
    ('test_dir', 'test_dir-modified'),
    ('test_dir2', 'test_dir2-modified'),
])
def test_apply_folder_name_scheme(observer_thread, folder_creation, expected_result):

    observer = observer_thread
    test_folder_dir = folder_creation

    head, tail = os.path.split(test_folder_dir)
    expected_path = os.path.join(head, expected_result)

    observer.join(timeout=OBSERVER_TIMEOUT)

    assert os.path.isdir(expected_path)


# @pytest.mark.eval
@pytest.mark.parametrize('file_name, expected_result', [
    ('test_file.py', 'test_file-modified.py'),
    ('test_file.js', 'test_file-modified.js'),
])
def test_apply_file_name_scheme(observer_thread, file_creation, expected_result):

    observer = observer_thread
    test_folder_dir = file_creation

    head, tail = os.path.split(test_folder_dir)
    expected_path = os.path.join(head, expected_result)

    observer.join(timeout=OBSERVER_TIMEOUT)

    assert os.path.isfile(expected_path)


# @pytest.mark.eval
@pytest.mark.parametrize('extension_by_folder', [
    {
        'video': ['.mkv', '.mov', '.mp4'],
        'audio': ['.mp3', '.mpa', '.ogg'],
        'text': ['.doc', '.odt', '.pdf'],
        'compressed_and_executable': ['.tar', '.z', '.zip', '.exe']
    }

])
def test_apply_file_sort(monkeypatch, observer_thread, batch_file_creation):
    observer = observer_thread
    toml = MockTOML()
    # monkeypatch.setattr(DirItem, '_get_directoryitem_config', toml.file_sort_conventions_map)
    observer.join(timeout=OBSERVER_TIMEOUT)
    os.listdir(TEST_PATH)


# @pytest.mark.eval
def test_create_temp_config():

    test_config = tmp_path / TEST_CONFIG_FILENAME

    with open(test_config, 'w+') as file:
        file.write(TEST_TOML)

    config = toml.load(test_config)
    diritem = DirItem(config)

    folder_paths = []

    for folder_path in diritem._get_file_sort_folder_structure():
        folder_paths.append(folder_path)

    print(folder_paths)
    assert True
