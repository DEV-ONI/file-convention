import sys
import os
import logging

from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
# from watchdog.events import LoggingEventHandler

path = '../test'

# walk will only recurse in directories which remain in dirnames
for file in os.walk(path, topdown=False):
    print(file)

class Conventions:

    def __init__(self, path):
        pass

class Folder

    def __init__(self, path):

    def apply_name_conventions():
        # name conventions for newly created files
        # name conventions for newly created folders
        pass

    def apply_folder_conventions():
        # content restrictions for newly created folders
        pass

    def apply_file_conventions():
        #
        pass

    def add_subdirectories():
        # add subdirectories to newly created folders
        pass

    def add_files():
        # add files to newly created folders
        pass

    def add_event_dispatch():
        pass
