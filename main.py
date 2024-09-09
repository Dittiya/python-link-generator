import threading
import time
import pyperclip
import os
from link_handler import handler
from typing import Callable, Type, Optional

def check_valid_link(link: str) -> bool:
    if link.startswith("https://"):
        return True
    return False

def link_handler_selection(url) -> Optional[Type]:
    if "fuckingfast.co" in url:
        return handler.FuckingFast
    if "datanodes.to" in url:
        return handler.Datanodes

    return None

def generate_link(content: str) -> str:
    dl_handler = link_handler_selection(content)
    if dl_handler == None:
        raise TypeError("No handler available for the URL")
    
    handle = dl_handler(content)
    link = handle.crawl()

    return link

def write_to_file(content: str, location: str="./links"):
    file_name = "/links.txt"
    if not os.path.exists(location):
        os.mkdir(location)

    link = generate_link(content)

    if not os.path.exists(location + file_name):
        with open(location + file_name, "w") as f:
            f.write(link)
    else:
        with open(location + file_name, "a") as f:
            f.write(f"\n{link}")

    return os.path.exists(location)


class ClipboardWatcher(threading.Thread):
    def __init__(self, predicate: Callable, callback: Callable, pause: float=5.0):
        super(ClipboardWatcher, self).__init__()
        self._predicate: Callable = predicate
        self._callback: Callable = callback
        self._pause: float = pause
        self._stopping: bool = False

    def run(self):
        recent_value: str = ""
        while not self._stopping:
            temp_value = pyperclip.paste()
            if temp_value != recent_value:
                recent_value = temp_value
                if self._predicate(recent_value):
                    self._callback(recent_value)

            time.sleep(self._pause)

    def stop(self):
        self._stopping = True

def main():
    watcher = ClipboardWatcher(check_valid_link, write_to_file, 0.5)

    watcher.start()
    while True:
        try:
            print("Watching clipboard...")
            time.sleep(5)
        except KeyboardInterrupt:
            watcher.stop()
            break

    return 0

if __name__ == "__main__":
    main()
