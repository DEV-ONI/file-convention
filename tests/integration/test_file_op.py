import pytest
import os
import time
import toml
from file_convention.monitor import begin_observer_thread, DirItem

OBSERVER_TIMEOUT = 5

TEST_CONFIG_FILENAME = 'test_conventions.toml'
TEST_PATH = './simulated_folder'


# urgent refactor needed to move observer fixture to TestClass level


@pytest.mark.eval
@pytest.mark.parametrize(
    'target_folders, folder_names, name_scheme, expected_name', [
        (['dir'], ['sub_dir1'], '{basename}-modified', 'sub_dir1-modified'),
        (['dir'], ['sub_dir2'], '{basename}-modified', 'sub_dir2-modified'),
    ]
)
def test_apply_folder_name_scheme(
    target_folders, folder_names, 
    name_scheme, expected_name,
    tempfolder_creation, generate_folder_name_config,
    batch_diritem_creation, observer_thread_method
    ):

    temp_dirs = tempfolder_creation
    config = generate_folder_name_config(temp_dirs, name_scheme)
    observer = observer_thread_method(config, temp_dirs)

    folder = batch_diritem_creation(
        temp_dirs, folder_names, 'folder'
    )

    observer.join(timeout=OBSERVER_TIMEOUT)

    for temp_dir in temp_dirs:
        expected_path = os.path.join(temp_dir, expected_name)

        assert os.path.isdir(expected_path)



@pytest.mark.eval
@pytest.mark.parametrize(
    'target_folders, file_names, name_scheme, expected_name', [
        (['dir'], ['file1'], '{basename}-modified', 'file1-modified'),
        (['dir'], ['file2'], '{basename}-modified', 'file2-modified'),
    ]
)
def test_apply_file_name_scheme(
    target_folders, file_names, 
    name_scheme, expected_name,
    tempfolder_creation, generate_file_name_config,
    batch_diritem_creation, observer_thread_method
    ):

    temp_dirs = tempfolder_creation
    config = generate_file_name_config(temp_dirs, name_scheme)
    observer = observer_thread_method(config, temp_dirs)

    print(f'file names: {file_names}')

    files = batch_diritem_creation(
        temp_dirs, file_names, 'file'
    )

    observer.join(timeout=OBSERVER_TIMEOUT)

    for temp_dir in temp_dirs:
        expected_path = os.path.join(temp_dir, expected_name)

        assert os.path.isfile(expected_path)



@pytest.mark.eval
@pytest.mark.parametrize('target_folders, file_map, filemove_map', [
    (
        ['dir'], {'subdir': ['.py', '.js']}, 
        {'file.py': 'subdir/file.py', 'file.js': 'subdir/file.js'}

    )
])
def test_apply_sort_convention(
    target_folders, file_map, 
    filemove_map, observer_thread_method, tempfolder_creation,
    batch_diritem_creation, generate_file_sort_config
    ):

    temp_dirs = tempfolder_creation
    config = generate_file_sort_config(temp_dirs, file_map)
    observer = observer_thread_method(config, temp_dirs)

    files = batch_diritem_creation(
        temp_dirs, filemove_map.keys(), 'file'
    )

    observer.join(timeout=OBSERVER_TIMEOUT)

    for temp_dir in temp_dirs:
        expected_files = [
            os.path.join(temp_dir, file) for file in filemove_map.values()
        ]

        assert False not in [os.path.isfile(file) for file in expected_files]








