import sys
import os
import shutil

import re
import toml

from pprint import pprint

from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
import watchdog.events as events

import threading
from functools import reduce

TEST_CONFIG = r'./tests/data/test_conventions.toml'
TEST_PATH = r'./simulated_folder'

FOLDER_CONVENTION_KEY = 'folder_convention'
FILE_CONVENTION_KEY = 'file_convention'
FOLDER_SORT_KEY = 'file_sort'


# event handler with overriden methods from the base filesystem event handler
class EventHandler(FileSystemEventHandler):

    def __init__(self, dir_handler, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.dir_item = dir_handler
        self.dir_item.apply_init_conventions()

    def on_any_event(self, event):

        # display event attributes
        event_attributes = (
            (event.event_type, event.src_path, event.dest_path)
            if event.event_type is events.FileModifiedEvent
            else (event.event_type, event.src_path, 'None')
        )
        # print('event type: {}, source path: {}, destination path: {}'.format(*event_attributes))

        if event.event_type == 'created':
            self.dir_item.apply_event_conventions(event.src_path)


class DirItem:

    def __init__(self, config):
        # dict mapping loaded from config file

        # possible refactor
        # self.config = config
        # self.conventions = self.config.get('conventions')
        # self.conventions_path_map = {convention.get('target_directory'): convention for convention in self.conventions}

        self.conventions = config
        self.conventions_path_map = self._get_convention_map()

    # side effect
    def _create_folders(self, folder_path):
        try:
            os.mkdir(folder_path)
        except FileExistsError:
            print('This file already exists')
            # do nothing
        finally:
            pass

    def apply_init_conventions(self):
        self._apply_target_directory_folder_structure()
        self._apply_file_sort_folder_structure()

    def _apply_target_directory_folder_structure(self):

        for folder_path in self.conventions_path_map.keys():
            self._create_folders(folder_path)

    def _get_file_sort_folder_structure(self):

        file_sort_mapping = self._get_convention_map(
            convention_type=FOLDER_CONVENTION_KEY,
            convention_name=FOLDER_SORT_KEY)

        print(file_sort_mapping)

        for path, filetype_sort_convention in file_sort_mapping.items():

            for folder in filetype_sort_convention.keys():
                folder_path = os.path.join(path, folder)
                yield folder_path

    def _apply_file_sort_folder_structure(self):

        for folder_path in self._get_file_sort_folder_structure():
            self._create_folders(folder_path)

    def apply_event_conventions(self, path):

        item_conventions = self._get_convention_by_type(path)
        renamed_path = self._apply_name_convention(path, item_conventions)
        self._apply_sort_convention(renamed_path, item_conventions)

    # pure function
    def _apply_name_convention(self, path, conventions):
        name_scheme = conventions.get('name_scheme')
        head, tail = os.path.split(path)

        if os.path.isfile(path):
            tail, ext = os.path.splitext(tail)
        else:
            ext = ''

        if name_scheme:
            renamed_path = os.path.join(head, name_scheme.format(basename=tail) + ext)
            os.rename(path, renamed_path)

            return renamed_path

    def _apply_duplicates_convention(self, conventions):
        pass

    def _apply_sort_convention(self, path, conventions):

        sort_scheme = conventions.get(FOLDER_SORT_KEY)
        sort_qualifier = None

        head, tail = os.path.split(path)
        root, ext = os.path.splitext(tail)

        # possible refactor
        if sort_scheme:
            for key, value in sort_scheme.items():
                if ext in value:
                    sort_qualifier = key
            if sort_qualifier:
                dest_path = os.path.join(head, sort_qualifier, tail)
                shutil.move(path, dest_path)

    def _get_convention_by_type(self, convention_type, path=''):

        conventions = {}
        try:
            head, tail = os.path.split(path)
            path_config = self.conventions_path_map[head]

            if os.path.isdir(path):
                conventions = path_config.get(FOLDER_CONVENTION_KEY)
            elif os.path.isfile(path) or os.path.islink(path):
                conventions = path_config.get(FILE_CONVENTION_KEY)
            else:
                conventions = path_config.get(FOLDER_CONVENTION_KEY)

        except KeyError as e:
            print(e)
            # do something here
        finally:
            return conventions

    def _get_convention_map(self, convention_type=None, convention_name=None):

        dir_conventions = {
            convention.get('target_directory'):
                recursive_get(
                    convention, convention_type, convention_name
                ) for convention in self.conventions
        }

        return dir_conventions


def recursive_get(item_map, *keys, default={}):
    keys = [key for key in keys if key is not None]
    if not len(keys):
        return item_map
    return reduce(lambda item_map, key: item_map.get(key, default), keys, item_map)


def begin_observer_thread(dir_handler):

    event_handler = EventHandler(dir_handler)
    observer = Observer()

    # an observer is called to a single parent directory.
    # the catch-all dispatch handles events for subdirectories
    observer.schedule(event_handler, TEST_PATH, recursive=True)

    return observer


if __name__ == '__main__':
    config = toml.load(TEST_CONFIG)
    dir_item = DirItem(config)
    observer = begin_observer_thread(dir_item)
    observer.start()
    observer.join()
