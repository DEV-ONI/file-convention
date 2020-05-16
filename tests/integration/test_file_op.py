import pytest
import os
import time
import toml
from file_convention.monitor import begin_observer_thread, DirItem

OBSERVER_TIMEOUT = 5

TEST_CONFIG_FILENAME = 'test_conventions.toml'


# @pytest.mark.integration
@pytest.mark.parametrize('folder_name, expected_result', [
    ('test_dir', 'test_dir-modified'),
    ('test_dir2', 'test_dir2-modified')
])
def test_apply_folder_scheme(observer_thread, folder_creation, expected_result):
    observer = observer_thread
    test_folder_dir = folder_creation

    head, tail = os.path.split(test_folder_dir)
    expected_path = os.path.join(head, expected_result)

    observer.join(timeout=OBSERVER_TIMEOUT)

    assert os.path.isdir(expected_path)


@pytest.mark.integration
@pytest.mark.parametrize(
    'file_names, expected_result',
    [
        ['test_file.py', 'test_file2.py',
         'test_file.js', 'test_file2.js', 'test_file.md',
         'test_file.toml', 'test_file.yaml']
    ]
)
def test_apply_file_sort(observer_thread, file_creation):
    observer = observer_thread
    # test_folder_dir = file_creation

    observer.join(timeout=OBSERVER_TIMEOUT)

    assert True


@pytest.mark.eval
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
