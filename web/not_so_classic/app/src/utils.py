import hashlib
import os
import signal
from flask import current_app
from werkzeug.datastructures import FileStorage

def md5FileHash(file: FileStorage) -> bytes:
    md5_hash = hashlib.md5()
    while chunk := file.read(8192):
        md5_hash.update(chunk)
    file.stream.seek(0)
    return md5_hash.digest()

def isValidURL(url: str):
    return url.startswith("http://") or url.startswith("https://") and len(url) < 512

def startAdmin(url: str):
    with open(current_app.config.get('FIFO_PATH'), mode='a') as fifo:
        fifo.write(f"{url}\n")
        os.kill(int(os.getenv('DAEMON_PID')), signal.SIGUSR1)