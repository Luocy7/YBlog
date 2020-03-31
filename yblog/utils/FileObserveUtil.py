# -*- coding:utf-8 _*-
"""
    @author: Luocy
    @time: 2020/03/31
    @copyright: © 2020 Luocy <luocy77@gmail.com>
"""

import time
import threading

from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

from yblog.task.task import file_created, file_deleted, file_modified, file_moved


class MyHandler(FileSystemEventHandler):
    def __init__(self, pattern=None):
        self.pattern = pattern or ".md"
        self.dummyThread = None

    def on_any_event(self, event):
        if not event.is_directory and event.src_path.endswith(self.pattern):
            print(event)

    def on_created(self, event):
        if not event.is_directory and event.src_path.endswith(self.pattern):
            file_created.delay(event.src_path)

    def on_deleted(self, event):
        if not event.is_directory and event.src_path.endswith(self.pattern):
            file_deleted.delay(event.src_path)

    def on_modified(self, event):
        if not event.is_directory and event.src_path.endswith(self.pattern):
            file_modified.delay(event.src_path)

    def on_moved(self, event):
        if not event.is_directory and event.src_path.endswith(self.pattern):
            file_moved.delay(event.src_path, event.dest_path)

    def start(self):
        self.dummyThread = threading.Thread(target=self._process)
        self.dummyThread.daemon = True
        self.dummyThread.start()

    @staticmethod
    def _process():
        while True:
            time.sleep(1)


handler = MyHandler()
handler.start()


def run_watcher(path):

    observer = Observer()
    observer.schedule(handler, path)
    observer.start()
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()


def run_with_thread(notepath):
    watcher_thread = threading.Thread(target=run_watcher, args=(notepath,))
    watcher_thread.start()


if __name__ == '__main__':
    run_watcher('.')
