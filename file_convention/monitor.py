import sys
import os
import shutil

import re
import toml

from pprint import pprint
# from logger import log_print

from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
import watchdog.events as events
# from watchdog.events import LoggingEventHandler

import threading

TEST_CONFIG = r'./tests/data/test_conventions.toml'
TEST_PATH = r'./simulated_folder'

FOLDER_CONVENTION_KEY = 'folder_convention'
FILE_CONVENTION_KEY = 'file_convention'
FOLDER_SORT_KEY = 'file_sort'


# event handler with overriden methods from the base filesystem event handler
class EventHandler(FileSystemEventHandler):

    def __init__(self, dir_handler):
        super().__init__()
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

        # for test
        self.config = config

        self.conventions = self.config.get('conventions')
        self.conventions_map = {convention['target_directory']: convention for convention in self.conventions}

    def _create_folders(self, folder_path):
        try:
            os.mkdir(folder_path)
        except FileExistsError:
            print('This file already exists')
        finally:
            pass

    def apply_init_conventions(self):
        self._apply_target_directory_folder_structure()
        self._apply_file_sort_folder_structure()

    def _apply_target_directory_folder_structure(self):

        for folder_path in self.conventions_map.keys():
            self._create_folders(folder_path)

    def _get_file_sort_folder_structure(self):

        for path, path_config in self.conventions_map.items():
            filetype_sort_convention = self._get_file_convention(path_config, key=FOLDER_SORT_KEY)

            if filetype_sort_convention:

                for folder in filetype_sort_convention.keys():
                    folder_path = os.path.join(path, folder)
                    yield folder_path

    def _apply_file_sort_folder_structure(self):

        for folder_path in self._get_file_sort_folder_structure():
            self._create_folders(folder_path)

    def apply_event_conventions(self, path):

        # test: path from keys must be valid, else error
        # test: folder conventions must be well formed, else continue
        # test: name_scheme must be defined, else ignore

        item_conventions = self._get_directoryitem_config(path)
        self._apply_name_convention(path, item_conventions)
        self._apply_sort_convention(path, item_conventions)

    def _apply_name_convention(self, path, conventions):
        name_scheme = conventions.get('name_scheme')
        head, tail = os.path.split(path)

        if os.path.isfile(path):
            root, ext = os.path.splitext(tail)

        if name_scheme:
            renamed_path = os.path.join(head, name_scheme.format(basename=root)+ext)
            os.rename(path, renamed_path)

    def _apply_duplicates_convention(self, conventions):
        pass

    def _apply_sort_convention(self, path, conventions):
        sort_scheme = conventions.get(FOLDER_SORT_KEY)
        head, tail = os.path.split(path)

        if os.path.isfile(path):
            root, ext = os.path.splitext(tail)

        # possible refactor
        if sort_scheme:
            for key, value in sort_scheme.items():
                if ext in value:
                    sort_qualifier = key
            if sort_qualifier:
                dest_path = os.path.join(head, sort_qualifier, tail)
                shutil.move(path, dest_path)

    def _apply_subdir_structure(self, conventions):
        pass

    def _get_file_convention(self, config, key=None):

        file_conventions = config.get(FILE_CONVENTION_KEY)

        if file_conventions:
            if key is not None:
                return file_conventions.get(key)
            else:
                print(file_conventions)
                return file_conventions
        else:
            return None

    def _get_folder_convention(self, config, key=None):

        folder_conventions = config.get(FOLDER_CONVENTION_KEY)

        if folder_conventions:
            if key:
                return folder_conventions.get(key)
            else:
                return folder_conventions
        else:
            return None

    def _get_path_config(self, path):

        try:
            head, tail = os.path.split(path)
            path_config = self.conventions_map[head]

            if os.path.isdir(path):
                conventions = self._get_folder_convention(path_config)
            elif os.path.isfile(path):
                conventions = self._get_file_convention(path_config)

        except KeyError as e:
            print(e)

        finally:
            pass

            return path_config

    def _get_directoryitem_config(self, path):
        conventions = {}
        try:
            head, tail = os.path.split(path)
            path_config = self.conventions_map[head]

            if os.path.isdir(path):
                conventions = self._get_folder_convention(path_config)
            elif os.path.isfile(path):
                conventions = self._get_file_convention(path_config)

        except KeyError as e:
            print(e)

        finally:
            return conventions


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
