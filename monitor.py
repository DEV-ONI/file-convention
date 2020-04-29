import sys
import logging

from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler, FileModifiedEvent
# from watchdog.events import LoggingEventHandler


# event handler with overriden methods from the base filesystem event handler
class EventHandler(FileSystemEventHandler):

    def __init__(self):
        super().__init__()

    def on_created(self, event):
        pass

    def on_deleted(self, event):
        pass

    def on_modified(self, event):
        pass

    def on_moved(self, event):
        pass

    def on_any_event(self, event):
        # display event attributes
        event_attributes = (
            (event.event_type, event.src_path, event.dest_path) if event.event_type is FileModifiedEvent
            else (event.event_type, event.src_path, 'None')
        )
        print(event_attributes)
        print('event type: {}, source path: {}, destination path: {}'.format(*event_attributes))


event_handler = EventHandler()
path = './test'

observer = Observer()
observer.schedule(event_handler, path, recursive=True)
observer.start()

try:
    while True:
        time.sleep(1)
except:
    pass

observer.join()
