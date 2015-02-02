#! /usr/bin/env python

import pyperclip
import gntp.notifier
from os.path import basename, dirname
import sys
import time
import logging
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
import hashlib


class ClipboardingEventHandler(FileSystemEventHandler):

    """Growl the events captured."""

    clip_digest = None

    def __init__(self, vimregister_filename='vimregister.txt'):
        self.vimregister_filename = vimregister_filename

    def copy_and_notify(self, clip):
        pyperclip.copy(clip)
        gntp.notifier.mini(
            "Copied %d characters to the clipboard" % len(clip),)

    def populate_clipboard(self, src_path):
        try:
            with open(src_path, "r") as file:
                clip = file.read().replace('\n', '\r\n')  # DOS linebreaks ...
                clip_digest = hashlib.md5(clip)
                # non-threaded hack to get rid of duplicate copies and
                # notifications... TODO if you copy a string from vim, and
                # overwrite the windows clipboard with something else locally,
                # and again copy an identical string from vim - it won't get
                # copied again ...
                if not self.__class__.clip_digest:
                    self.__class__.clip_digest = clip_digest
                    logging.info("Initializing the clip digest")
                    self.copy_and_notify(clip)
                elif (clip_digest.digest() ==
                      self.__class__.clip_digest.digest()
                      ):
                    logging.warning("Duplicate clip digest. Not copying.")
                else:
                    self.__class__.clip_digest = clip_digest
                    self.copy_and_notify(clip)
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
