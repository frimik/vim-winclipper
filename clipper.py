#! /usr/bin/env python

import pyperclip
import gntp.notifier
from os.path import basename, dirname
import sys
import time
import logging
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler


class ClipboardingEventHandler(FileSystemEventHandler):
    """Growl the events captured."""

    def __init__(self, vimregister_filename='vimregister.txt'):
        self.vimregister_filename = vimregister_filename

    @staticmethod
    def populate_clipboard(src_path):
        try:
            with open(src_path, "r") as file:
                clip = file.read()
                pyperclip.copy(clip.replace('\n', '\r\n'))
                gntp.notifier.mini(
                    "Copied %d characters to the clipboard" % len(clip),)
        except IOError as e:
            logging.error("Error: %r", e)
            return

    def on_modified(self, event):
        if basename(event.src_path) == self.vimregister_filename:
            self.populate_clipboard(event.src_path)

    def on_moved(self, event):
        what = 'directory' if event.is_directory else 'file'
        if basename(event.dest_path) == self.vimregister_filename:
            gntp.notifier.mini(
                "Moved %s: from %s to %s" % (what, event.src_path,
                                             event.dest_path),)

    def on_created(self, event):
        what = 'directory' if event.is_directory else 'file'
        if basename(event.src_path) == self.vimregister_filename:
            gntp.notifier.mini("Created %s: %s" % (what, event.src_path),)

    def on_deleted(self, event):
        what = 'directory' if event.is_directory else 'file'
        if basename(event.src_path) == self.vimregister_filename:
            gntp.notifier.mini("Deleted %s: %s" % (what, event.src_path),)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO,
                        format='%(asctime)s - %(message)s',
                        datefmt='%Y-%m-%d %H:%M:%S')
    path = sys.argv[1] if len(sys.argv) > 1 else '.'
    event_handler = ClipboardingEventHandler(basename(path))
    observer = Observer()
    observer.schedule(event_handler, dirname(path), recursive=False)
    observer.start()
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()
