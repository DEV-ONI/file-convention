import sys
import os
import logging

from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
# from watchdog.events import LoggingEventHandler

path = './test'

# walk will only recurse in directories which remain in dirnames
for file in os.walk(path, topdown=False):
    print(file)


def apply_file_conventions():
    pass

`def apply_folder_conventions()
    pass
