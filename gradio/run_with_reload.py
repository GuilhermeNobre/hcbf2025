import os
import sys
import time

from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

class ReloadHandler(FileSystemEventHandler):
    def on_modified(self, event):
        if event.src_path.endswith(".py"):
            print("\033[1;32mArquivo modificado, reiniciando...\033[0m")
            os.system("pkill -f 'python3 main.py'")  # Mata o processo atual
            os.system("python3 main.py &")  # Reinicia o script

if __name__ == "__main__":
    path = "."  # Diretório atual
    event_handler = ReloadHandler()
    observer = Observer()
    observer.schedule(event_handler, path, recursive=False)
    observer.start()
    try:
        os.system("python3 main.py &")  # Inicia o script Gradio pela primeira vez
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()