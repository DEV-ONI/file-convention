import pytest
import os
import sys
import threading
import toml
from functools import reduce

from file_convention.monitor import DirItem

from file_convention.monitor import begin_observer_thread
from file_convention.monitor import EventHandler

from file_convention.monitor import recursive_get

TEST_PATH = './simulated_folder'
DATA_PATH = './tests/data'
TEST_CONFIG = os.path.join(DATA_PATH, 'test_conventions.toml')
FOLDER_CONVENTION_KEY = 'folder_convention'
FILE_CONVENTION_KEY = 'file_convention'
FILE_SORT_KEY = 'file_sort'
NAME_SCHEME_KEY = 'name_scheme'
DUPLICATES_SCHEME_KEY = 'duplicates_scheme'
TARGET_DIRECTORY_KEY = 'target_directory'


@pytest.fixture(scope='function')
def generate_file_sort_conventions(args_list):

    file_sort_conventions = []

    for tagret_path, file_sort_mapping in args_list:

        file_sort_convention = {
            'target_directory': tagret_path,
            'folder_convention': {'file_sort': file_sort_mapping}
        }
        file_sort_conventions.append(file_sort_convention)

    return file_sort_conventions


def test_observer_thread(observer_thread):
    assert observer_thread in threading.enumerate()


# @pytest.mark.unit
@pytest.mark.parametrize('convention_type, config', [
    ('file_convention', {'file_convention': True, 'folder_convention': False}),
    ('folder_convention', {'file_convention': False, 'folder_convention': True})
])
def test_get_convention_by_type(monkeypatch, convention_type, config):
    dir_handler = DirItem({})
    monkeypatch.setattr(dir_handler, 'conventions_map', config)
    result = dir_handler._get_convention_by_type(convention_type)

    assert result


@pytest.mark.unit
@pytest.mark.parametrize('keys, mapping_object', [
    (['key1', 'key2', 'key3'], {'key1': {'key2': {'key3': 'target_val'}}}),
    ([], 'target_val')
])
def test_recursive_get(mapping_object, keys):
    assert recursive_get(mapping_object, *keys) == 'target_val'


@pytest.mark.unit
@pytest.mark.parametrize('keys, mapping_object', [
    (['file_convention', 'convention'], [
        {'target_directory': 1, 'file_convention': {'convention': 1}},
        {'target_directory': 2, 'file_convention': {'convention': 2}}
    ]),
    (['file_convention'], [
        {'target_directory': 1, 'file_convention': 1}
    ])
])
def test_get_convention_map(monkeypatch, mapping_object, keys):
    dir_handler = DirItem({})
    monkeypatch.setattr(dir_handler, 'conventions', mapping_object)

    result = dir_handler._get_convention_map(*keys)

    assert all([key == value for key, value in result.items()])


@pytest.mark.unit
@pytest.mark.parametrize('target_paths, args_list', [
    (
        ['./folder/subfolder', './folder/subfolder2'],
        [('./folder', {'subfolder': ['.py'], 'subfolder2': ['.py']})]
    ),
    (
        ['./folder/subfolder', './folder2/subfolder2'],
        [('./folder', {'subfolder': ['.py']}), ('./folder2', {'subfolder2': ['.py']})]
    )
])
def test_get_file_sort_folder_structure(
        monkeypatch,
        target_paths,
        generate_file_sort_conventions):

    dir_handler = DirItem({})

    # fixture function accepts parametrize arguments
    conventions = generate_file_sort_conventions

    monkeypatch.setattr(dir_handler, 'conventions', conventions)
    paths = [path for path in dir_handler._get_file_sort_folder_structure()]

    assert paths == target_paths

"""
@pytest.mark.unit
@pytest.mark.parametrize('expected_paths, folder_mapping', [
    (
        [TEST_PATH+'/subpath1', TEST_PATH+'/subpath2'],
        {'subpath1': ['.txt'], 'subpath2': ['.pdf']}
    )
])
def test_get_file_sort_folder_structure(
        monkeypatch, generate_file_sort_dict, expected_paths):

    dir_handler = DirItem({})
    monkeypatch.setattr(dir_handler, 'conventions', generate_file_sort_dict)

    assert expected_paths == [folder_path for folder_path in dir_handler._get_file_sort_folder_structure()]
"""

"""
@pytest.mark.eval
@pytest.mark.parametrize('keys, mapping_object', [
    ([None], {
        'target_directory': 'specified_path', 'file_convention': 'target_val'}),
    (['convention'], {
        'target_directory': 'path', 'file_convention': {'convention': 'target_val'}
    }),
    (['convention', 'sub_convention'], {
        'target_directory': 'path', 'file_convention':
            {'convention': {'sub_convention': 'target_val'}}
    })
])
def test_get_convention_by_type(keys, mapping_object):
    dir_handler = DirItem({})

    result = dir_handler._get_file_convention(mapping_object, *keys)
    print(result)
    assert result == 'target_val'
"""
