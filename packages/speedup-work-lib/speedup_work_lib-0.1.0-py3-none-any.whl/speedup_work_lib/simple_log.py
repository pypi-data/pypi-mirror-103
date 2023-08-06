#!/usr/bin/env python
"""
.. current_module:: simple_log.py
.. created_by:: Darren Xie
.. created_on:: 04/25/2021

This python script is a simple log.
"""
import sys
from datetime import datetime

TIME_FORMAT = '%H:%M:%S'


class SimpleLog:
    """
    Basic log class
    """
    start_time = ''

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def start_log(self):
        """print out start time"""
        self.start_time = datetime.now()
        sys.stdout.write(f"Starting process at {self._curr_time()}\n")
        self.break_section()

    def print_log(self, msg=''):
        """print out the log message"""
        sys.stdout.write(f"[{self._curr_time()}]: {msg}\n")

    def stop_log(self):
        """print out duration time"""
        duration = datetime.now() - self.start_time
        self.break_section()
        sys.stdout.write(f"Done to spend time: {str(duration)}\n")

    def _curr_time(self):
        """
        return: current time
        """
        return datetime.now().strftime(TIME_FORMAT)

    def break_section(self):
        """
        :return: break section lines
        """
        return '-' * 120
