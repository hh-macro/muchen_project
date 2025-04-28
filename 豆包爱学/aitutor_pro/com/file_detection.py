import os
import time
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler


class Watcher:
    def __init__(self, path_name):
        self.DIRECTORY_TO_WATCH = path_name  # 文件夹路径
        self.observer = Observer()

    def run(self):
        event_handler = Handler()
        self.observer.schedule(event_handler, self.DIRECTORY_TO_WATCH, recursive=True)
        self.observer.start()
        try:
            while True:
                time.sleep(5)
        except KeyboardInterrupt:
            self.observer.stop()
            print("监查停止!")
        finally:
            event_handler.save_filenames_to_file()
        self.observer.join()


class Handler(FileSystemEventHandler):
    def __init__(self):
        self.filenames = []  # 文件名列表

    def on_any_event(self, event):
        if event.is_directory:
            return None

        filename = os.path.basename(event.src_path)
        if filename not in self.filenames:
            self.filenames.append(filename)

        if event.event_type == 'created':
            # 当文件被创建时触发
            print(f"创建的事件被触发 - {event.src_path}\t 文件名:\t {filename}")

        elif event.event_type == 'modified':
            # 当文件被修改时触发
            print(f"修改的事件被触发 - {event.src_path}\t 文件名: {filename}")

    def save_filenames_to_file(self):
        with open("detected_filenames.txt", "w", encoding="utf-8") as file:
            filenames_str = str(self.filenames)
            file.write(filenames_str)
        print("文件名列表已保存到 detected_filenames.txt")


if __name__ == "__main__":
    path_name = r"C:\Users\macroh\AppData\Roaming\Reqable\tmp"
    w = Watcher(path_name)
    w.run()
