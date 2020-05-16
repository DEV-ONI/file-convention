import pytest
import os
import sys
import threading
import toml


from file_convention.monitor import begin_observer_thread
from file_convention.monitor import EventHandler


def test_observer_thread(observer_thread):
    assert observer_thread in threading.enumerate()

"""
test_monitor = TestMonitor()
test_monitor.test_on_event()
"""

# clear_folder()
